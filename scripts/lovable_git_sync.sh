#!/usr/bin/env bash
#
# lovable_git_sync.sh — Riversa il contenuto di uno ZIP dentro un repository
# Git locale (clone del progetto collegato a Lovable/GitHub) e fa push.
#
# Uso:
#   scripts/lovable_git_sync.sh -z /path/al/progetto.zip -r /path/al/repo/clonato [opzioni]
#
# Opzioni:
#   -z, --zip PATH        Percorso dello ZIP da estrarre (obbligatorio)
#   -r, --repo PATH       Percorso del repository Git locale, già clonato (obbligatorio)
#   -b, --branch NAME     Branch su cui fare push (default: quello corrente del repo)
#   -m, --message MSG     Messaggio di commit (default: "Sync from <nome_zip> (<data>)")
#   -y, --yes             Non chiedere conferma prima di svuotare la cartella di destinazione
#   -n, --dry-run         Mostra cosa farebbe, senza modificare nulla
#   -h, --help            Mostra questo aiuto
#
# Cosa fa:
#   1. Estrae lo ZIP in una cartella temporanea.
#   2. Se lo ZIP contiene un'unica cartella radice, ne "appiattisce" il contenuto
#      (caso tipico degli export che avvolgono tutto in una cartella con lo
#      stesso nome dello ZIP).
#   3. Svuota il repository di destinazione, preservando SEMPRE la directory .git.
#   4. Copia il contenuto estratto nel repository.
#   5. git add -A, commit e push sul branch indicato.
#
# Il repository di destinazione deve essere già un clone Git valido (contenere
# una cartella .git): lo script si rifiuta di procedere altrimenti.

set -euo pipefail

usage() {
    sed -n '2,26p' "$0" | sed 's/^# \{0,1\}//'
    exit "${1:-0}"
}

ZIP_PATH=""
REPO_DIR=""
BRANCH=""
COMMIT_MSG=""
ASSUME_YES=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        -z|--zip) ZIP_PATH="$2"; shift 2 ;;
        -r|--repo) REPO_DIR="$2"; shift 2 ;;
        -b|--branch) BRANCH="$2"; shift 2 ;;
        -m|--message) COMMIT_MSG="$2"; shift 2 ;;
        -y|--yes) ASSUME_YES=1; shift ;;
        -n|--dry-run) DRY_RUN=1; shift ;;
        -h|--help) usage 0 ;;
        *) echo "Opzione sconosciuta: $1" >&2; usage 1 ;;
    esac
done

if [[ -z "$ZIP_PATH" || -z "$REPO_DIR" ]]; then
    echo "Errore: --zip e --repo sono obbligatori." >&2
    usage 1
fi

if [[ ! -f "$ZIP_PATH" ]]; then
    echo "Errore: file ZIP non trovato: $ZIP_PATH" >&2
    exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
    echo "Errore: 'unzip' non è installato." >&2
    exit 1
fi

REPO_DIR="$(cd "$REPO_DIR" 2>/dev/null && pwd || true)"
if [[ -z "$REPO_DIR" ]]; then
    echo "Errore: la cartella --repo non esiste." >&2
    exit 1
fi

if [[ ! -d "$REPO_DIR/.git" ]]; then
    echo "Errore: '$REPO_DIR' non contiene una cartella .git." >&2
    echo "Questo script sincronizza solo dentro un clone Git già esistente." >&2
    exit 1
fi

if [[ -z "$BRANCH" ]]; then
    BRANCH="$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD)"
fi

if [[ -z "$COMMIT_MSG" ]]; then
    COMMIT_MSG="Sync from $(basename "$ZIP_PATH") ($(date '+%Y-%m-%d %H:%M'))"
fi

echo "== lovable_git_sync =="
echo "ZIP di origine : $ZIP_PATH"
echo "Repo di destino: $REPO_DIR"
echo "Branch         : $BRANCH"
echo "Commit message : $COMMIT_MSG"
[[ $DRY_RUN -eq 1 ]] && echo "(modalità dry-run: nessuna modifica verrà applicata)"
echo

TMP_DIR="$(mktemp -d)"
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "-> Estrazione ZIP in $TMP_DIR"
unzip -q -o "$ZIP_PATH" -d "$TMP_DIR"

# Se lo zip contiene un'unica cartella radice, appiattiscila.
shopt -s nullglob dotglob
entries=("$TMP_DIR"/*)
shopt -u dotglob
if [[ ${#entries[@]} -eq 1 && -d "${entries[0]}" ]]; then
    echo "-> Rilevata singola cartella radice nello ZIP, la appiattisco"
    FLAT_DIR="$(mktemp -d)"
    shopt -s dotglob nullglob
    mv "${entries[0]}"/* "$FLAT_DIR"/ 2>/dev/null || true
    shopt -u dotglob nullglob
    rm -rf "$TMP_DIR"
    TMP_DIR="$FLAT_DIR"
fi

if [[ $DRY_RUN -eq 1 ]]; then
    echo
    echo "Contenuto che verrebbe copiato in $REPO_DIR:"
    find "$TMP_DIR" -mindepth 1 -maxdepth 2 | sed "s#^$TMP_DIR#  #"
    echo
    echo "Dry-run completato. Nessuna modifica applicata."
    exit 0
fi

if [[ $ASSUME_YES -ne 1 ]]; then
    echo "ATTENZIONE: tutto il contenuto di '$REPO_DIR' (eccetto .git) verrà eliminato"
    echo "e sostituito con quello estratto dallo ZIP."
    read -r -p "Continuare? [y/N] " reply
    case "$reply" in
        [yY]|[yY][eE][sS]) ;;
        *) echo "Annullato."; exit 1 ;;
    esac
fi

echo "-> Svuotamento di $REPO_DIR (esclusa .git)"
find "$REPO_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

echo "-> Copia del nuovo contenuto"
shopt -s dotglob nullglob
for item in "$TMP_DIR"/*; do
    cp -a "$item" "$REPO_DIR"/
done
shopt -u dotglob nullglob

echo "-> git add / commit / push"
git -C "$REPO_DIR" add -A

if git -C "$REPO_DIR" diff --cached --quiet; then
    echo "Nessuna modifica da committare."
    exit 0
fi

git -C "$REPO_DIR" commit -m "$COMMIT_MSG"
git -C "$REPO_DIR" push -u origin "$BRANCH"

echo
echo "Fatto. Push completato su origin/$BRANCH."
