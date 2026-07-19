"""Automazione del sito Stitch con Playwright.

Replica il flusso manuale:
    apri Stitch -> nuovo progetto -> seleziona modello (es. "3.1 pro")
    -> seleziona versione (web/app) -> allega reference + primo prompt -> invia
    -> attendi generazione -> invia i prompt successivi in sequenza (animazioni)
    -> preleva il risultato (codice / screenshot / link)

IMPORTANTE — I SELETTORI:
    I "selettori" (i punti su cui cliccare/scrivere) sono TUTTI in config.yaml,
    sezione stitch.selectors. Vanno calibrati sull'interfaccia reale di Stitch:
    apri Stitch nel browser, usa l'ispettore, e aggiorna i selettori nel config.
    Il codice qui sotto NON va toccato per la calibrazione: basta il config.

Login:
    La sessione (login Google/Stitch) è salvata in stitch.user_data_dir tramite
    un "persistent context" di Playwright. Fai il login una volta con
    `python -m src.stitch.login`, poi il bot riusa quella sessione.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from ..config import Config

if TYPE_CHECKING:
    from ..prompt_builder import PromptStep

log = logging.getLogger(__name__)


class StitchBrowser:
    """Wrapper attorno a un browser Playwright puntato su Stitch."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.url = cfg.get("stitch.url", "https://stitch.withgoogle.com/")
        self.model = cfg.get("stitch.model", "3.1 pro")
        self.version = cfg.get("stitch.version", "web")
        self.headless = bool(cfg.get("stitch.headless", True))
        self.user_data_dir = cfg.get("stitch.user_data_dir", "./.stitch_profile")
        self.slow_mo = int(cfg.get("stitch.slow_mo_ms", 0))
        self.nav_timeout = int(cfg.get("stitch.timeouts.navigation_ms", 60000))
        self.gen_timeout = int(cfg.get("stitch.timeouts.generation_ms", 900000))
        self.sel = cfg.get("stitch.selectors", {}) or {}

        self._playwright = None
        self._context = None
        self._page = None

    # ---- ciclo di vita -----------------------------------------------------

    def __enter__(self) -> "StitchBrowser":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def start(self) -> None:
        from playwright.sync_api import sync_playwright

        Path(self.user_data_dir).mkdir(parents=True, exist_ok=True)
        self._playwright = sync_playwright().start()
        # persistent context = riusa la sessione di login salvata su disco
        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        self._context.set_default_timeout(self.nav_timeout)
        self._page = self._context.pages[0] if self._context.pages else self._context.new_page()

    def close(self) -> None:
        try:
            if self._context:
                self._context.close()
        finally:
            if self._playwright:
                self._playwright.stop()
            self._context = None
            self._page = None
            self._playwright = None

    # ---- helper selettori --------------------------------------------------

    def _selector(self, key: str, **fmt) -> str:
        raw = self.sel.get(key)
        if not raw:
            raise RuntimeError(
                f"Selettore '{key}' non configurato in stitch.selectors (config.yaml)."
            )
        return raw.format(**fmt) if fmt else raw

    def _click(self, key: str, **fmt) -> None:
        selector = self._selector(key, **fmt)
        log.debug("click %s -> %s", key, selector)
        self._page.click(selector)

    def _maybe_click(self, key: str, **fmt) -> bool:
        """Clicca se il selettore è configurato e presente; altrimenti passa oltre."""
        if not self.sel.get(key):
            return False
        try:
            self._page.click(self._selector(key, **fmt), timeout=self.nav_timeout)
            return True
        except Exception as exc:  # noqa: BLE001
            log.debug("click opzionale '%s' non riuscito: %s", key, exc)
            return False

    # ---- azioni ad alto livello -------------------------------------------

    def open(self) -> None:
        log.info("Apro Stitch: %s", self.url)
        self._page.goto(self.url, wait_until="domcontentloaded")

    def new_project(self) -> None:
        self._maybe_click("new_project_button")

    def select_model(self, model: Optional[str] = None) -> None:
        model = model or self.model
        if self._maybe_click("model_menu_button"):
            self._maybe_click("model_option", model=model)
            log.info("Modello selezionato: %s", model)

    def select_version(self, version: Optional[str] = None) -> None:
        version = (version or self.version).lower()
        key = "version_web_toggle" if version == "web" else "version_app_toggle"
        if self._maybe_click(key):
            log.info("Versione selezionata: %s", version)

    def send_step(self, step: "PromptStep", is_first: bool) -> None:
        """Allega le immagini (se presenti), scrive il prompt e invia."""
        if step.images:
            self._attach_images(step.images)

        prompt_selector = self._selector("prompt_input")
        self._page.fill(prompt_selector, step.text)
        self._click("submit_button")
        log.info("Prompt inviato (immagini: %d).", len(step.images))
        self._wait_generation_done()

    def _attach_images(self, images: list[Path]) -> None:
        upload_selector = self._selector("image_upload_input")
        paths = [str(p) for p in images if Path(p).exists()]
        if not paths:
            return
        # set_input_files accetta più file insieme
        self._page.set_input_files(upload_selector, paths)
        log.info("Allegate %d reference.", len(paths))

    def _wait_generation_done(self) -> None:
        """Attende che Stitch finisca di generare."""
        done_selector = self.sel.get("generation_done")
        if not done_selector:
            # nessun selettore di "fine": attesa prudente basata sul network idle
            self._page.wait_for_load_state("networkidle", timeout=self.gen_timeout)
            return
        self._page.wait_for_selector(done_selector, timeout=self.gen_timeout)

    # ---- risultato ---------------------------------------------------------

    def collect_result(self, result_type: str, dest_dir: Path) -> Optional[Path]:
        """Preleva il risultato dalla pagina secondo result.type."""
        dest_dir.mkdir(parents=True, exist_ok=True)

        if result_type == "none":
            return None

        if result_type == "screenshot":
            out = dest_dir / "screen.png"
            self._page.screenshot(path=str(out), full_page=True)
            return out

        if result_type == "link":
            out = dest_dir / "link.txt"
            link = self._page.url
            sel = self.sel.get("result_link")
            if sel:
                try:
                    link = self._page.get_attribute(sel, "href") or link
                except Exception:  # noqa: BLE001
                    pass
            out.write_text(link + "\n", encoding="utf-8")
            return out

        if result_type == "code":
            out = dest_dir / "code.html"
            code = self._copy_code()
            if code is None:
                # fallback: salva l'HTML della pagina
                code = self._page.content()
            out.write_text(code, encoding="utf-8")
            return out

        raise ValueError(f"result.type sconosciuto: {result_type!r}")

    def _copy_code(self) -> Optional[str]:
        """Clicca 'Copy code' e legge la clipboard, se il selettore è configurato."""
        if not self.sel.get("copy_code_button"):
            return None
        try:
            self._click("copy_code_button")
            return self._page.evaluate("navigator.clipboard.readText()")
        except Exception as exc:  # noqa: BLE001
            log.warning("Copia codice non riuscita: %s", exc)
            return None

    # ---- orchestrazione di un intero job ----------------------------------

    def run_job(self, steps: list["PromptStep"], result_type: str, dest_dir: Path,
                model: Optional[str] = None, version: Optional[str] = None) -> Optional[Path]:
        """Esegue l'intero flusso per un job e restituisce il path del risultato."""
        self.open()
        self.new_project()
        self.select_model(model)
        self.select_version(version)

        for index, step in enumerate(steps):
            self.send_step(step, is_first=(index == 0))

        return self.collect_result(result_type, dest_dir)
