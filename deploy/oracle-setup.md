# Deploy su Oracle Cloud (VM 24/7)

Guida passo-passo per far girare il bot in continuazione su una VM Oracle Cloud
(le stesse istruzioni valgono per qualsiasi VM Linux Ubuntu).

---

## 0) Prerequisiti

- Una VM Oracle Cloud **Always Free** (Ubuntu 22.04 va benissimo).
- Accesso SSH alla VM.
- Sul **tuo PC** (con schermo): Python + questo progetto, per fare il login a Stitch una volta.

---

## 1) Prepara la VM

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
# Dipendenze di sistema per Chromium (Playwright)
sudo apt install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
  libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
  libasound2 libpango-1.0-0 libcairo2 libatspi2.0-0
```

## 1-bis) Installazione rapida (uno script)

In alternativa ai passi manuali, dopo aver clonato il progetto puoi lanciare:
```bash
bash deploy/install.sh
```
Fa tutto: dipendenze, virtualenv, librerie, Chromium, `config.yaml` e `.env`.

## 2) Scarica il progetto

```bash
cd ~
git clone <URL_DEL_TUO_REPO> stitch-bot
cd stitch-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## 2-bis) ARSENAL — portalo sulla VM (rclone da Google Drive)

Su Colab l'arsenal si "montava" da Drive; su una VM va **copiato una volta**.
Il modo più semplice è **rclone**:

```bash
sudo apt install -y rclone
rclone config          # crea un remote chiamato "gdrive" (tipo: drive), autorizza col browser
# scarica SOLO l'arsenal (non tutto il Drive) nella cartella locale ./arsenal
rclone copy "gdrive:percorso/della/cartella senza nome 6" ~/stitch-bot/arsenal --progress
```

Poi in `config.yaml`:
```yaml
roulette:
  enabled: true
  arsenal_base: "/home/ubuntu/stitch-bot/arsenal"
```

> L'arsenal è grande (diversi GB): assicurati di avere spazio disco sulla VM.
> Quando aggiungi materiale su Drive, rilancia lo stesso `rclone copy` per aggiornarlo.

## 3) Configura

```bash
cp config.example.yaml config.yaml
cp .env.example .env
# modifica config.yaml (sorgente, modello, selettori) e .env (ANTHROPIC_API_KEY se serve)
nano config.yaml
```

## 4) Login a Stitch — il punto delicato

Stitch richiede il login con Google. Da un IP di datacenter (come Oracle) Google
spesso **blocca** il login automatico. Soluzione affidabile: fai il login **sul tuo PC**
e copia la sessione sulla VM.

**Sul tuo PC** (con schermo):
```bash
python -m src.stitch.login      # si apre un browser: fai il login, poi premi INVIO
```
Questo crea la cartella `.stitch_profile/`.

**Copia la sessione sulla VM:**
```bash
# dal tuo PC
tar czf stitch_profile.tgz .stitch_profile
scp stitch_profile.tgz ubuntu@<IP_VM>:~/stitch-bot/
# sulla VM
cd ~/stitch-bot && tar xzf stitch_profile.tgz
```

> Se un giorno Google chiede di riautenticarti, ripeti il login sul PC e ricopia
> la cartella. È il metodo più stabile, dato che Stitch non ha un'API ufficiale.

## 5) Prova al volo (una passata sola)

```bash
source .venv/bin/activate
python -m src.main --once
```

Controlla i log e la cartella `results/`.

## 6) Attiva il servizio 24/7

```bash
sudo cp deploy/stitch-bot.service /etc/systemd/system/stitch-bot.service
# adatta User e i percorsi dentro il file se necessario
sudo nano /etc/systemd/system/stitch-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now stitch-bot
journalctl -u stitch-bot -f          # log in tempo reale
```

Fatto: il bot ora gira in continuazione, cerca nuovi job e li invia a Stitch.

---

## Note utili

- **Aggiornare il codice:** `git pull && sudo systemctl restart stitch-bot`
- **Fermare:** `sudo systemctl stop stitch-bot`
- **Selettori Stitch cambiati?** aggiorna `stitch.selectors` in `config.yaml`, poi riavvia.
- **Materiale da Google Drive:** metti `source.type: gdrive` in config.yaml, e condividi
  la cartella Drive con l'email del service account (vedi README).
