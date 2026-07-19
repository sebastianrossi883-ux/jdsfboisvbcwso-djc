# Stitch Reference Mirroring System

Un programma che **invia in automatico prompt e reference a [Stitch](https://stitch.withgoogle.com/)**,
in sequenza (base → animazioni), e gira **in continuazione** su una VM (es. Oracle Cloud).

Tu prepari il materiale (immagini reference + file `.md` con i prompt); il
programma apre Stitch nel browser, seleziona il modello e la versione, incolla
reference e prompt uno dopo l'altro, e salva il risultato.

---

## Come funziona (in breve)

```
  material/<nome_job>/            ← un "job" = una cartella
     refs/*.png|*.jpg             ← reference (immagini)
     01_....md, 02_....md, ...    ← prompt, inviati in ordine
     job.yaml                     ← (opzionale) definisce ordine e override
        │
        ▼
  [ programma ]  ── apre Stitch ──►  seleziona "3.1 pro" + versione web
        │                            allega reference + 1° prompt → invia
        │                            invia i prompt successivi in sequenza
        ▼
  results/<nome_job>/              ← risultato (codice / screenshot / link)
```

Il programma **non inventa i prompt**: usa i tuoi file `.md` così come sono
(`prompt.mode: passthrough`). In opzione può farli rielaborare a Claude
(`prompt.mode: claude`).

---

## Dove carico il materiale

Ogni **job** è una cartella con dentro:

- le **immagini** reference (`.png`, `.jpg`, …) — vengono allegate al **primo** prompt;
- uno o più file **`.md`** = i prompt, inviati **in ordine alfabetico** (usa i prefissi `01_`, `02_`, …);
- (facoltativo) un **`job.yaml`** per controllare esattamente ordine, reference e override di modello/versione.

Due posti possibili (si sceglie in `config.yaml`, sezione `source`):

1. **Locale** → metti le cartelle-job dentro `material/`.
2. **Google Drive** → una cartella "madre" su Drive, con una sottocartella per ogni job.
   Il programma le scarica da solo. Devi **condividere** la cartella Drive con
   l'email del *service account* (vedi sotto).

C'è già un esempio completo pronto in **`material/esempio_job/`** (basato sul
materiale reale del progetto cantina).

## Dove trovo il risultato

In **`results/<nome_job>/`**. Cosa viene salvato dipende da `result.type` in `config.yaml`:

| `result.type` | Cosa salva                          |
|---------------|-------------------------------------|
| `code`        | il codice esportato (`code.html`)   |
| `screenshot`  | screenshot del design (`screen.png`)|
| `link`        | il link al progetto (`link.txt`)    |
| `none`        | niente (il risultato resta su Stitch)|

---

## Installazione (locale, per provarlo)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

cp config.example.yaml config.yaml     # poi modificalo
cp .env.example .env                    # serve solo se usi prompt.mode: claude
```

### Login a Stitch (una volta sola)

Stitch richiede il login Google. Si fa **una volta** e la sessione viene salvata:

```bash
python -m src.stitch.login     # si apre un browser: fai il login, poi premi INVIO
```

### Prova

```bash
python -m src.main --once      # elabora i job in coda una volta e esce
```

Poi, per il funzionamento 24/7 su Oracle Cloud, segui **[deploy/oracle-setup.md](deploy/oracle-setup.md)**.

---

## Configurazione

Tutto è in `config.yaml` (parti da `config.example.yaml`). Sezioni principali:

- **`source`** — da dove arriva il materiale (`local` o `gdrive`).
- **`stitch`** — url, `model` (`"3.1 pro"`), `version` (`web`/`app`), `headless`,
  timeout e — importante — i **`selectors`**.
- **`prompt`** — `passthrough` (default) o `claude`.
- **`result`** — cosa salvare.
- **`loop`** — `poll_interval_sec`, `once`.

### ⚠️ I selettori di Stitch (da calibrare)

I `stitch.selectors` in `config.yaml` sono la mappa dei punti su cui il programma
clicca/scrive nella pagina di Stitch (pulsante nuovo progetto, menu modello,
campo prompt, upload immagini, invio, ecc.). Quelli forniti sono **ipotesi**:
vanno adattati all'interfaccia reale di Stitch (apri Stitch, usa l'ispettore del
browser e aggiorna i valori). **Non serve toccare il codice**, solo il config.

> Hai il vecchio script che già funzionava? Incollamelo: ricavo i selettori
> esatti e li metto nel config, così l'automazione parte al primo colpo.

### Google Drive (opzionale)

1. Crea un *service account* su Google Cloud e scarica il JSON delle credenziali
   → salvalo come `gdrive-service-account.json`.
2. Abilita la **Google Drive API** sul progetto.
3. **Condividi** la cartella Drive (quella "madre") con l'email del service account.
4. In `config.yaml`: `source.type: gdrive` e metti `source.gdrive.folder_id`.

---

## Struttura del progetto

```
src/
  main.py               loop 24/7 (entry point)
  config.py             caricamento config.yaml + .env
  job.py                modello "job" (reference + prompt in ordine)
  prompt_builder.py     costruisce la sequenza di prompt (+ opz. Claude)
  results.py            cartella dei risultati
  sources/
    local.py            job da cartella locale
    gdrive.py           job da Google Drive
  stitch/
    browser.py          automazione del sito Stitch (Playwright)
    login.py            login una-tantum (salva la sessione)
config.example.yaml     configurazione di esempio
material/esempio_job/   un job completo di esempio
deploy/                 servizio systemd + guida Oracle Cloud
results/                output
```

---

## Note oneste sui limiti

- **Stitch non ha un'API pubblica ufficiale**: la consegna avviene automatizzando
  il browser. È funzionante ma va calibrata sui selettori reali.
- **Login su cloud**: Google può bloccare il login automatico da IP di datacenter.
  Per questo il login si fa sul PC e si copia la sessione sulla VM (vedi guida deploy).
- Se Stitch aggiorna l'interfaccia, potresti dover ritoccare i `selectors` nel config.
