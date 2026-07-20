"""Prova REALE dal vivo: manda UN prompt a Stitch e clicca "Genera progetti".

Verifica l'automazione vera: browser visibile (sei già loggato), imposta Web,
forza il modello 3.1 Pro (gate anti-Flash), scrive il prompt e invia. Non
aspetta la generazione completa: ti lascia il browser aperto ~40s per guardare.

Uso:
    python -m src.stitch.test_send
    python -m src.stitch.test_send "Il tuo prompt qui"
"""

from __future__ import annotations

import sys
import time

from .sender import ModelDowngradeError, StitchSender

DEFAULT_PROMPT = (
    "Crea un sito web elegante e cinematografico per un ristorante italiano di "
    "lusso, stile editoriale da rivista, tipografia raffinata."
)


def main() -> None:
    from ..config import Config, load_config

    prompt = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROMPT

    try:
        cfg = load_config()
    except FileNotFoundError:
        cfg = load_config("config.example.yaml")

    if isinstance(cfg, Config):
        st = cfg.data.setdefault("stitch", {})
        st["headless"] = False               # visibile, per guardare
        if not st.get("browser_channel"):
            st["browser_channel"] = "chrome"  # Chrome vero (login gia' salvato)

    print("Apro Stitch... (sei gia' loggato)")
    with StitchSender(cfg) as sender:
        sender.open()

        print("Aspetto che Stitch carichi...")
        if sender._find("prompt_input", timeout=60000) is None:  # noqa: SLF001
            print("Non vedo il campo del prompt. Fai il login nella finestra e riprova.")
            return

        # 1) versione Web (non App)
        sender.select_version("web")

        # 2) forza il modello 3.1 Pro
        try:
            sender.ensure_model_pro()
            print("OK: modello impostato su 3.1 Pro.")
        except ModelDowngradeError as exc:
            print("ATTENZIONE:", exc)
            print("Provo comunque a inviare, ma potrebbe usare un altro modello.")

        # 3) scrivi il prompt e invia (pulsante o tasto Invio)
        print("Scrivo il prompt e invio...")
        try:
            sender._fill("prompt_input", prompt)      # noqa: SLF001
            sender.submit()
            print("\n✅ PROMPT INVIATO! Guarda la finestra di Chrome: "
                  "Stitch dovrebbe iniziare a generare il sito.")
        except Exception as exc:  # noqa: BLE001
            print("\n❌ Qualcosa non ha funzionato:", exc)
            print("Salvo un debug per capire cosa aggiustare.")

        sender.save_debug("test_send")
        print("\nLascio il browser aperto 40 secondi per guardare...")
        time.sleep(40)

    print("Fatto.")


if __name__ == "__main__":
    main()
