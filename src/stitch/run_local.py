"""Esegue il FLUSSO VERO in locale, dal vivo, per vedere se gira tutto.

Manda i 5 prompt (prompts/01..05) a Stitch in sequenza, browser visibile,
sceglie Web e prova 3.1 Pro (se non ci riesce, prosegue e stampa i modelli del
menu per capire come si chiama). Le reference sono opzionali.

Uso:
    python -m src.stitch.run_local
    python -m src.stitch.run_local /percorso/cartella/con/reference

Nota: la generazione di Stitch richiede minuti; tra una fase e l'altra il
programma aspetta (phase_wait). Guarda la finestra di Chrome.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from ..prompt_builder import PromptStep
from .sender import StitchSender

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
PROMPT_FILES = [
    "01_sito_da_reference.md",
    "02_animate_gsap.md",
    "03_guest_component.md",
    "04_framer_interactive.md",
    "05_correzione_finale.md",
]


def _load_prompts(prompts_dir: Path) -> list[str]:
    texts = []
    for name in PROMPT_FILES:
        f = prompts_dir / name
        texts.append(f.read_text(encoding="utf-8") if f.exists() else f"(manca {name})")
    return texts


def _load_references(folder: Path | None) -> list[Path]:
    if folder is None or not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMG_EXT)


def main() -> None:
    from ..config import Config, load_config

    ref_arg = sys.argv[1] if len(sys.argv) > 1 else None
    references = _load_references(Path(ref_arg) if ref_arg else None)

    try:
        cfg = load_config()
    except FileNotFoundError:
        cfg = load_config("config.example.yaml")

    if isinstance(cfg, Config):
        st = cfg.data.setdefault("stitch", {})
        st["headless"] = False                 # visibile
        if not st.get("browser_channel"):
            st["browser_channel"] = "chrome"    # Chrome vero
        st["model_gate_strict"] = False         # per questo test: prosegui anche senza 3.1 Pro

    prompts = _load_prompts(Path("prompts"))
    steps = [PromptStep(text=t, images=(references if i == 0 else []))
             for i, t in enumerate(prompts)]

    print(f"Prompt caricati: {len(steps)} | reference: {len(references)}")
    print("Apro Stitch (browser visibile)...")

    with StitchSender(cfg) as sender:
        sender.open()
        if sender._find("prompt_input", timeout=60000) is None:  # noqa: SLF001
            print("Non vedo il campo del prompt. Fai il login e riprova.")
            return

        sender.select_version("web")
        print("Versione: Web.")

        for index, step in enumerate(steps):
            phase = index + 1
            print(f"\n===== FASE {phase}/{len(steps)} =====")
            try:
                sender.send_prompt(step.text, images=step.images)
                print(f"Fase {phase} inviata.")
            except Exception as exc:  # noqa: BLE001
                print(f"Fase {phase}: problema -> {exc}")
                sender.save_debug(f"run_local_fase{phase}")
                break
            if phase < len(steps):
                print(f"Aspetto {sender.phase_wait}s prima della fase successiva...")
                time.sleep(sender.phase_wait)

        print("\nLascio il browser aperto 60 secondi per guardare il risultato...")
        time.sleep(60)

    print("Fatto.")


if __name__ == "__main__":
    main()
