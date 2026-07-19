"""Login una-tantum a Stitch, per salvare la sessione riusata poi dal bot.

Uso (sul TUO PC, con interfaccia grafica):

    python -m src.stitch.login

Si apre un browser NON headless: fai il login con Google fino a vedere la
dashboard di Stitch, poi premi INVIO nel terminale. La sessione viene salvata
in stitch.user_data_dir (default: ./.stitch_profile).

Per il server Oracle (che di solito non ha interfaccia grafica): fai il login
qui sul tuo PC e poi copia la cartella .stitch_profile sulla VM. Vedi il README.
"""

from __future__ import annotations

from pathlib import Path

from ..config import load_config


def main() -> None:
    from playwright.sync_api import sync_playwright

    cfg = load_config()
    url = cfg.get("stitch.url", "https://stitch.withgoogle.com/")
    user_data_dir = cfg.get("stitch.user_data_dir", "./.stitch_profile")
    Path(user_data_dir).mkdir(parents=True, exist_ok=True)

    print(f"Apro un browser su {url}")
    print("Fai il login con Google fino alla dashboard di Stitch, poi torna qui.")

    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,  # deve essere visibile per fare il login a mano
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(url, wait_until="domcontentloaded")

        input("\n>> Quando hai completato il login, premi INVIO qui per salvare la sessione... ")

        context.close()

    print(f"\nSessione salvata in: {user_data_dir}")
    print("Ora il bot potrà usare Stitch senza rifare il login (finché la sessione è valida).")


if __name__ == "__main__":
    main()
