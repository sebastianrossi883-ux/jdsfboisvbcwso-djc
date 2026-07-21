# Sincronizzazione con Lovable via Git (aggiornamento offline)

Lovable offre una sincronizzazione bidirezionale con un repository GitHub
collegato al progetto: un `git push` sul branch principale del repo aggiorna
automaticamente i file del progetto e la relativa anteprima, senza passare
dalla chat dell'IA. Questo è utile quando si vuole aggiornare il codice del
progetto a partire da un file `.zip` (es. un export locale) senza doverlo
ricaricare manualmente nella chat.

Lo script `scripts/lovable_git_sync.sh` automatizza il flusso:

1. Estrae lo ZIP in una cartella temporanea (e appiattisce l'eventuale
   cartella radice unica che molti export includono).
2. Svuota il repository locale di destinazione **preservando sempre** la
   cartella `.git`.
3. Copia dentro il repo il contenuto estratto.
4. Fa `git add`, `commit` e `push` verso `origin` sul branch indicato.

## Prerequisiti

- Il progetto Lovable deve già essere collegato a un repository GitHub
  (dalle impostazioni del progetto su Lovable).
- Devi avere un clone locale di quel repository, con le credenziali Git
  già configurate per il push (es. SSH key o token salvato).

## Uso

```bash
scripts/lovable_git_sync.sh \
  --zip ~/Downloads/progetto-export.zip \
  --repo ~/dev/mio-progetto-lovable \
  --branch main
```

Opzioni principali:

| Opzione          | Descrizione                                                  |
|------------------|----------------------------------------------------------------|
| `-z, --zip`      | Percorso dello ZIP da riversare (obbligatorio)                |
| `-r, --repo`     | Cartella del clone Git locale del progetto (obbligatorio)     |
| `-b, --branch`   | Branch di destinazione (default: branch corrente del repo)    |
| `-m, --message`  | Messaggio di commit personalizzato                             |
| `-y, --yes`      | Salta la conferma prima di svuotare la cartella di destinazione |
| `-n, --dry-run`  | Mostra cosa verrebbe copiato, senza modificare nulla           |

Per prudenza lo script:

- si rifiuta di girare su una cartella che non contiene già una `.git`
  (non crea repository nuovi, aggiorna solo cloni esistenti);
- chiede conferma prima di cancellare il contenuto del repo (salta con `-y`
  se vuoi usarlo in automatico, es. da un altro script);
- supporta `--dry-run` per verificare cosa cambierebbe prima di applicare.

## Nota sui costi Lovable

Il push su GitHub aggiorna i file del progetto Lovable come sincronizzazione
passiva, senza passare per l'elaborazione dell'IA in chat. Per i dettagli
aggiornati su crediti di build/cloud e piani, fai sempre riferimento alla
documentazione ufficiale di Lovable, perché le policy dei piani possono
cambiare nel tempo.
