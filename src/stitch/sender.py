"""Sender per Stitch (ricostruzione in Playwright, Linux/Colab-friendly).

Replica il flusso documentato del vecchio `send_to_stitch.py` (macOS):

  apri Stitch -> attendi login Google -> per ogni fase:
     seleziona/forza il modello "3.1 Pro" (gate anti-downgrade a "3 Flash")
     [fase 1] allega le reference (le fette) + invia il prompt
     [fasi 2..5] invia i prompt successivi in sequenza
     attendi la generazione, poi attendi `phase_wait_seconds`
  a fine ciclo: scarica lo ZIP del risultato.

DIFFERENZE VOLUTE rispetto all'originale:
  - niente automazione macOS (osascript/pbcopy): qui si digita/clicca con
    Playwright dentro l'iframe di Stitch, così gira anche su Linux/Colab;
  - i selettori sono tutti in config (stitch.selectors) e accettano PIU'
    candidati: il codice prova il primo che esiste. Vanno calibrati una volta
    sulla pagina reale di Stitch (vedi `save_debug`, salva screenshot + DOM).

NON contiene i testi dei prompt: quelli stanno nei file in `prompts/` (o nel
job), così restano tuoi e modificabili senza toccare questo motore.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional, Sequence

from ..config import Config

log = logging.getLogger(__name__)


class ModelDowngradeError(RuntimeError):
    """Sollevata quando non si riesce a tenere il modello su "3.1 Pro"."""


def _as_list(value) -> list[str]:
    """Normalizza un selettore in lista di candidati."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


class StitchSender:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.url = cfg.get("stitch.url", "https://stitch.withgoogle.com/")
        self.model = cfg.get("stitch.model", "3.1 Pro")
        self.version = str(cfg.get("stitch.version", "web")).lower()  # "web" oppure "app"
        self.headless = bool(cfg.get("stitch.headless", True))
        self.channel = cfg.get("stitch.browser_channel", None)  # es. "chrome"; None = Chromium
        self.user_data_dir = cfg.get("stitch.user_data_dir", "./.stitch_profile")
        self.slow_mo = int(cfg.get("stitch.slow_mo_ms", 0))
        self.nav_timeout = int(cfg.get("stitch.timeouts.navigation_ms", 60000))
        self.gen_timeout = int(cfg.get("stitch.timeouts.generation_ms", 900000))
        self.phase_wait = int(cfg.get("stitch.phase_wait_seconds", 180))
        self.download_timeout = int(cfg.get("stitch.download_timeout_seconds", 1800))
        self.model_gate_retries = int(cfg.get("stitch.model_gate_retries", 3))
        self.sel = cfg.get("stitch.selectors", {}) or {}
        self.debug_dir = Path(cfg.get("stitch.debug_dir", "./debug"))

        self._playwright = None
        self._context = None
        self._page = None

    # ---- ciclo di vita -----------------------------------------------------

    def __enter__(self) -> "StitchSender":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def start(self) -> None:
        from playwright.sync_api import sync_playwright

        Path(self.user_data_dir).mkdir(parents=True, exist_ok=True)
        self._playwright = sync_playwright().start()
        launch_kwargs = dict(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            slow_mo=self.slow_mo,
            accept_downloads=True,
            # Nasconde i segnali di automazione: Google altrimenti blocca il login
            # ("browser non sicuro").
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
            ignore_default_args=["--enable-automation"],
        )
        if self.channel:  # usa Chrome vero se richiesto e disponibile
            launch_kwargs["channel"] = self.channel
        try:
            self._context = self._playwright.chromium.launch_persistent_context(**launch_kwargs)
        except Exception:
            launch_kwargs.pop("channel", None)  # fallback a Chromium
            self._context = self._playwright.chromium.launch_persistent_context(**launch_kwargs)

        # ulteriore mascheramento: nasconde navigator.webdriver
        try:
            self._context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            )
        except Exception:  # noqa: BLE001
            pass

        self._context.set_default_timeout(self.nav_timeout)
        self._page = self._context.pages[0] if self._context.pages else self._context.new_page()

    def close(self) -> None:
        try:
            if self._context:
                self._context.close()
        finally:
            if self._playwright:
                self._playwright.stop()
            self._context = self._page = self._playwright = None

    # ---- helper su frame/selettori ----------------------------------------

    def _frames(self):
        """Tutti i contesti dove cercare: pagina + iframe (Stitch vive in iframe)."""
        yield self._page
        for frame in self._page.frames:
            if frame is not self._page.main_frame:
                yield frame

    def _find(self, keys: str, timeout: int = 4000):
        """Trova il primo elemento visibile tra i candidati, in pagina o iframe.

        `keys` è la chiave in stitch.selectors; il valore può essere una stringa
        o una lista di selettori candidati.
        """
        candidates = _as_list(self.sel.get(keys))
        deadline = time.time() + timeout / 1000
        while time.time() < deadline:
            for ctx in self._frames():
                for selector in candidates:
                    try:
                        loc = ctx.locator(selector).first
                        if loc.count() > 0 and loc.is_visible():
                            return loc
                    except Exception:
                        continue
            time.sleep(0.25)
        return None

    def _click(self, keys: str, timeout: int = 8000, required: bool = True) -> bool:
        loc = self._find(keys, timeout=timeout)
        if loc is None:
            if required:
                self.save_debug(f"missing_{keys}")
                raise RuntimeError(f"Selettore '{keys}' non trovato (calibra stitch.selectors).")
            return False
        loc.click()
        return True

    def _fill(self, keys: str, text: str, timeout: int = 8000) -> None:
        loc = self._find(keys, timeout=timeout)
        if loc is None:
            self.save_debug(f"missing_{keys}")
            raise RuntimeError(f"Campo '{keys}' non trovato (calibra stitch.selectors).")
        loc.click()
        loc.fill(text)

    # ---- login -------------------------------------------------------------

    def open(self) -> None:
        log.info("Apro Stitch: %s", self.url)
        self._page.goto(self.url, wait_until="domcontentloaded")

    def wait_for_login(self, timeout_ms: Optional[int] = None) -> None:
        """Attende che compaia il composer (campo prompt) = login completato."""
        timeout_ms = timeout_ms or self.nav_timeout
        log.info("Attendo il composer di Stitch (fai il login se richiesto)...")
        loc = self._find("prompt_input", timeout=timeout_ms)
        if loc is None:
            self.save_debug("no_composer")
            raise RuntimeError("Composer non trovato: login non riuscito o UI cambiata.")
        log.info("Composer pronto.")

    # ---- versione Web / App (si sceglie una volta) ------------------------

    def select_version(self, version: Optional[str] = None) -> None:
        """Sceglie la versione del progetto: "web" (default) oppure "app".

        A differenza del modello, la versione si imposta UNA volta (è una scelta
        del progetto, non cambia ad ogni prompt).
        """
        version = (version or self.version).lower()
        key = "version_web_toggle" if version == "web" else "version_app_toggle"
        if self._click(key, timeout=6000, required=False):
            log.info("Versione selezionata: %s", version)
        else:
            log.info("Toggle versione '%s' non trovato (forse gia' impostata o UI diversa).", version)

    # ---- gate sul modello 3.1 Pro -----------------------------------------

    def ensure_model_pro(self) -> None:
        """Seleziona e verifica il modello 3.1 Pro prima di un invio.

        Riproduce il gate del sistema originale:
          - se il composer mostra già 3.1 Pro -> ok
          - se mostra Flash / altro -> riseleziona 3.1 Pro
          - se non riesce a tenerlo -> ModelDowngradeError (invio annullato)
        """
        target = self.model
        for attempt in range(1, self.model_gate_retries + 1):
            if self._model_is(target):
                log.info("OK: il composer mostra gia' %s", target)
                return
            log.warning("ATTENZIONE: il composer NON e' su %s (tentativo %d)", target, attempt)
            self._select_model(target)
            time.sleep(1.0)
        if self._model_is(target):
            log.info("OK: %s confermato dopo riselezione", target)
            return
        self.save_debug("pre_send_model_downgrade")
        raise ModelDowngradeError(
            f"STOP: non riesco a tenere {target} (quota finita?). Invio annullato di proposito."
        )

    def _model_is(self, name: str) -> bool:
        """Verifica se l'etichetta del modello attivo contiene `name`."""
        loc = self._find("model_current_label", timeout=3000)
        if loc is None:
            return False
        try:
            txt = (loc.inner_text() or "").strip().lower()
            return name.lower() in txt
        except Exception:
            return False

    def _select_model(self, name: str) -> None:
        """Apre il menu del modello e seleziona `name` (es. "3.1 Pro").

        Robusto anche se non conosco l'etichetta esatta: dopo aver aperto il
        menu, cerca una voce breve che contenga "Pro" (o il nome cercato) ed
        escluda "progetti". Se non trova, stampa le voci viste (per diagnosi).
        """
        if not self._click("model_menu_button", timeout=6000, required=False):
            log.warning("Non sono riuscito ad aprire il menu del modello.")
            return
        time.sleep(0.9)

        # 1) prova i selettori configurati per l'opzione
        option_loc = self._find("model_option", timeout=3000)
        if option_loc is not None:
            option_loc.click()
            log.info("Modello selezionato tramite selettore configurato.")
            return

        # 2) fallback: cerca la voce "Pro" nel menu appena aperto
        wanted = name.lower()
        key = "pro" if "pro" in wanted else wanted
        selectors = "[role='option'], [role='menuitem'], [role='menuitemradio'], li, button"
        seen: list[str] = []
        for ctx in self._frames():
            try:
                elements = ctx.query_selector_all(selectors)
            except Exception:
                continue
            for el in elements:
                try:
                    txt = (el.inner_text() or "").strip()
                except Exception:
                    continue
                low = txt.lower()
                if not txt or len(txt) > 30 or "progett" in low:
                    continue
                seen.append(txt)
                if key in low or wanted in low:
                    try:
                        el.click()
                        log.info("Modello selezionato dal menu: %r", txt)
                        return
                    except Exception:
                        continue

        # niente da cliccare: stampa cosa c'era nel menu (diagnosi)
        uniq = sorted(set(seen))
        log.warning("Voce '%s' non trovata. Voci brevi viste nel menu: %s", name, uniq[:40])

    # ---- invio (pulsante o tastiera) --------------------------------------

    def submit(self) -> None:
        """Invia il prompt: prova il pulsante, poi la tastiera (Invio)."""
        loc = self._find("submit_button", timeout=3000)
        if loc is not None:
            loc.click()
            log.info("Inviato col pulsante.")
            return
        inp = self._find("prompt_input", timeout=3000)
        if inp is None:
            raise RuntimeError("Ne' pulsante di invio ne' campo prompt trovati.")
        inp.click()
        self._page.keyboard.press("Enter")
        log.info("Inviato con il tasto Invio (nessun pulsante trovato).")

    # ---- invio prompt ------------------------------------------------------

    def attach_references(self, images: Sequence[Path]) -> None:
        paths = [str(p) for p in images if Path(p).exists()]
        if not paths:
            return
        loc = self._find("image_upload_input", timeout=6000)
        if loc is None:
            self.save_debug("missing_image_upload_input")
            raise RuntimeError("Input upload immagini non trovato (calibra stitch.selectors).")
        loc.set_input_files(paths)
        log.info("Allegate %d reference.", len(paths))

    def send_prompt(self, text: str, images: Optional[Sequence[Path]] = None) -> None:
        """Un invio completo: gate modello -> allega -> scrivi -> invia -> attendi."""
        self.ensure_model_pro()
        if images:
            self.attach_references(images)
        self._fill("prompt_input", text)
        self.submit()
        log.info("Prompt inviato (%d caratteri, %d immagini).", len(text), len(images or []))
        self._wait_generation_done()

    def _wait_generation_done(self) -> None:
        done = self._find("generation_done", timeout=self.gen_timeout)
        if done is None:
            # nessun marker di fine: fallback su network idle
            try:
                self._page.wait_for_load_state("networkidle", timeout=self.gen_timeout)
            except Exception:
                pass

    # ---- download risultato ------------------------------------------------

    def download_result(self, dest_dir: Path) -> Optional[Path]:
        dest_dir.mkdir(parents=True, exist_ok=True)
        try:
            with self._page.expect_download(timeout=self.download_timeout * 1000) as info:
                self._click("download_button")
            download = info.value
            out = dest_dir / (download.suggested_filename or "stitch_result.zip")
            download.save_as(str(out))
            # traccia l'ultimo download, come nell'originale
            (dest_dir / "LAST_STITCH_DOWNLOAD_PATH.txt").write_text(str(out) + "\n", encoding="utf-8")
            log.info("ZIP scaricato: %s", out)
            return out
        except Exception as exc:  # noqa: BLE001
            log.warning("Download non riuscito: %s", exc)
            self.save_debug("download_failed")
            return None

    # ---- debug -------------------------------------------------------------

    def save_debug(self, tag: str) -> None:
        """Salva screenshot + DOM di TUTTI i frame (Stitch vive in un iframe)."""
        try:
            self.debug_dir.mkdir(parents=True, exist_ok=True)
            stamp = time.strftime("%Y%m%d_%H%M%S")
            base = self.debug_dir / f"{stamp}_{tag}"
            self._page.screenshot(path=str(base) + ".png", full_page=True)
            for i, ctx in enumerate(self._frames()):
                try:
                    html = ctx.content()
                    (Path(str(base) + f"_frame{i}.html")).write_text(html, encoding="utf-8")
                except Exception:
                    continue
            log.info("Debug salvato: %s*", base)
        except Exception as exc:  # noqa: BLE001
            log.debug("save_debug fallito: %s", exc)

    # ---- orchestrazione dell'intero job -----------------------------------

    def run_job(self, steps: Sequence, dest_dir: Path, download: bool = True) -> Optional[Path]:
        """Esegue le fasi in sequenza. `steps` = lista di PromptStep (text, images)."""
        self.open()
        self.wait_for_login()
        self.select_version()   # sceglie "web" (non "app") una volta

        for index, step in enumerate(steps):
            phase = index + 1
            log.info("=== FASE %d/%d ===", phase, len(steps))
            self.send_prompt(step.text, images=getattr(step, "images", None))
            if phase < len(steps):
                log.info("Attendo %ds prima della fase successiva...", self.phase_wait)
                time.sleep(self.phase_wait)

        if download:
            return self.download_result(dest_dir)
        return None
