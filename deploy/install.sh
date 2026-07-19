#!/usr/bin/env bash
# Installazione unica del bot su una VM Linux (Oracle Cloud Always Free, Ubuntu).
# Uso:
#   bash deploy/install.sh
# Idempotente: puoi rilanciarlo. NON scarica l'arsenal (vedi oracle-setup.md, passo rclone).

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
echo ">> Progetto: $PROJECT_DIR"

echo ">> [1/5] Dipendenze di sistema..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip git \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
  libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
  libpango-1.0-0 libcairo2 libatspi2.0-0

echo ">> [2/5] Virtualenv + librerie Python..."
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ">> [3/5] Browser per Playwright (Chromium)..."
python -m playwright install chromium

echo ">> [4/5] File di configurazione..."
[ -f config.yaml ] || { cp config.example.yaml config.yaml; echo "   creato config.yaml (modificalo!)"; }
[ -f .env ] || { cp .env.example .env; echo "   creato .env"; }

echo ">> [5/5] Fatto."
cat <<'NEXT'

Prossimi passi (vedi deploy/oracle-setup.md):
  1) Porta l'arsenal sulla VM con rclone           (passo "ARSENAL")
  2) Copia il profilo di login Stitch dal tuo PC    (passo "LOGIN")
  3) Modifica config.yaml (roulette.arsenal_base, selettori, ecc.)
  4) Prova:   source .venv/bin/activate && python -m src.main --once
  5) Attiva il servizio 24/7:
       sudo cp deploy/stitch-bot.service /etc/systemd/system/stitch-bot.service
       sudo systemctl daemon-reload && sudo systemctl enable --now stitch-bot
       journalctl -u stitch-bot -f
NEXT
