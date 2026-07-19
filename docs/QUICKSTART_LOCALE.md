# Prova in locale (sul tuo PC)

Obiettivo: far girare e **controllare** il programma sul tuo computer, prima di
metterlo su Google Colab. Ora è pronto per essere provato lo **splitter** delle
reference (il resto — invio a Stitch — arriva quando carichi `send_to_stitch.py`).

---

## 1) Scarica il programma

```bash
git clone https://github.com/sebastianrossi883-ux/jdsfboisvbcwso-djc.git
cd jdsfboisvbcwso-djc
git checkout claude/f-4alo1r
```

## 2) Ambiente Python

**Mac / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Pillow
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install Pillow
```

## 3) Prova lo splitter su una tua reference vera

Metti una o più reference (screenshot lunghi di siti) in una cartella, poi:

```bash
python -m src.reference_splitter /PERCORSO/DELLE/REFERENCE ./out_fette 3
```

- 1° argomento: la cartella con le reference (`.jpg`, `.png`, `.webp`)
- 2° argomento: dove salvare le fette
- 3° argomento: in quante parti dividere (default 3)

## 4) Controlla il risultato

Le fette sono in:
```
out_fette/<nome-reference>/parte-1-di-3.png
                           parte-2-di-3.png
                           parte-3-di-3.png
out_fette/INDICE_SPLIT.md
```
La **HERO** è sempre nella `parte-1`. Apri le immagini e verifica che il taglio
sia come lo vuoi. Se vuoi fette diverse, cambia il numero (es. `4`) o l'overlap
(`--overlap 0.05`).

---

## Prova veloce senza reference tue (immagine finta)

Per verificare che tutto giri, puoi generare al volo uno screenshot finto:

```bash
python -c "from PIL import Image,ImageDraw; im=Image.new('RGB',(1280,3600),'white'); d=ImageDraw.Draw(im); [d.rectangle([0,i*1200,1280,(i+1)*1200],fill=c) for i,c in enumerate(['#8B0000','#DAA520','#2F4F4F'])]; im.save('finta.jpg')"
mkdir -p REF_TEST && mv finta.jpg REF_TEST/
python -m src.reference_splitter REF_TEST ./out_fette 3
```

Devi ottenere 3 fette in `out_fette/finta/`.

---

## Dopo (invio a Stitch)

L'invio a Stitch userà il tuo `send_to_stitch.py` **intatto**. Sul Mac lo lanci
già col suo `.command`. Per il porting su Colab serve prima caricare quel file su
Drive (vedi README principale).
