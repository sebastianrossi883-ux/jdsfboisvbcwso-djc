# I 5 prompt (le fasi di Stitch)

Il sender invia **5 prompt in sequenza**, come il sistema originale. Ogni file
qui è una **fase**: incollaci dentro il tuo testo esatto del prompt.

| File | Fase | Cosa fa (dal flusso originale) |
|---|---|---|
| `01_sito_da_reference.md` | 1 | Genera il **sito dalle reference** (le fette allegate a questa fase) |
| `02_animate_gsap.md` | 2 | `/animate` + regia GSAP Awwwards + GSAP master + manifesto |
| `03_guest_component.md` | 3 | Protocollo Ironclad + **1 solo Guest Component** come nuova section |
| `04_framer_interactive.md` | 4 | **1 solo Framer Interactive** originale, senza cambiare la struttura |
| `05_correzione_finale.md` | 5 | Correzione finale motion/componenti/menu/link/bug, senza ridisegnare |

**Le reference** (le fette prodotte dallo splitter) vengono allegate **solo alla
fase 1**, esattamente come nel flusso originale.

Puoi anche mettere questi 5 file dentro la cartella di un singolo job (con le
reference), invece che qui: il programma li invia nell'ordine `01..05`.

> Questi testi sono **tuoi**: il motore (`src/stitch/sender.py`) non li tocca.
> Sostituisci il contenuto di ogni file col tuo prompt reale.
