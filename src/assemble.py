"""Assemblaggio: dalla scelta della roulette ai 5 prompt da inviare a Stitch.

La roulette sceglie un componente e un framer (dall'arsenal su Drive/VM). Qui si
legge il loro codice sorgente e lo si "impacchetta" nei prompt delle fasi 3 e 4,
nello stesso formato del tuo `selected_component_for_stitch.md`:

    Selected: `<nome>`
    ## ORIGINAL FILE: `path/al/file`
    SHA256: `...`
    ```lang
    <codice>
    ```

Le fasi 1, 2, 5 restano i prompt fissi in `prompts/`. La fase 3 = componente
assemblato, la fase 4 = framer assemblato.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

log = logging.getLogger(__name__)

# estensioni sorgente da includere, con il linguaggio per il blocco markdown
SOURCE_LANG = {
    ".tsx": "tsx", ".jsx": "jsx", ".ts": "ts", ".js": "javascript",
    ".css": "css", ".scss": "scss", ".html": "html",
}
SKIP_DIRS = {"node_modules", "dist", "build", ".git", "__MACOSX", ".next"}
MAX_FILE_BYTES = 200_000          # salta file sorgente enormi
MAX_FILES = 12                     # non impacchettare più di N file per componente


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def _iter_source_files(root: Path) -> list[Path]:
    """File sorgente rilevanti, ordinati con i 'principali' (App/index/main) per primi."""
    files: list[Path] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SOURCE_LANG:
            files.append(p)

    def score(p: Path) -> tuple:
        name = p.name.lower()
        main = any(k in name for k in ("app", "index", "main"))
        # sorgenti prima dei css; "main" prima di tutto
        is_code = p.suffix.lower() in (".tsx", ".jsx", ".ts", ".js")
        return (0 if main else 1, 0 if is_code else 1, str(p))

    return sorted(files, key=score)[:MAX_FILES]


def _file_block(path: Path, root: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        log.debug("skip %s: %s", path, exc)
        return None
    if len(content.encode("utf-8", "replace")) > MAX_FILE_BYTES:
        return None
    rel = path.relative_to(root)
    lang = SOURCE_LANG.get(path.suffix.lower(), "")
    return (
        f"## ORIGINAL FILE: `{rel}`\n"
        f"SHA256: `{_sha256(content)}`\n\n"
        f"```{lang}\n{content}\n```\n"
    )


def assemble_component(folder: Path, header: str) -> str:
    """Impacchetta un guest component nel prompt della fase 3."""
    folder = Path(folder)
    parts = [header.rstrip(), "", f"Selected: `{folder.name}`", ""]
    blocks = [b for f in _iter_source_files(folder) if (b := _file_block(f, folder))]
    if not blocks:
        parts.append("_(nessun file sorgente trovato in questo componente)_")
    else:
        parts.extend(blocks)
    return "\n".join(parts).rstrip() + "\n"


def assemble_framer(folder: Path, header: str) -> str:
    """Impacchetta un Framer interactive nel prompt della fase 4."""
    return assemble_component(folder, header)


# intestazioni (le regole d'oro) delle fasi 3 e 4
COMPONENT_HEADER = (
    "# VERIFIED ORIGINAL GUEST COMPONENT\n\n"
    "**REGOLA D'ORO ZERO-DISTRUZIONE & SCROLL-SAFE:**\n"
    "1. Questo componente va AGGIUNTO come NUOVA `<section>` in più.\n"
    "2. VIETATO cancellare/sostituire le sezioni esistenti per fargli posto.\n"
    "3. NON metterlo come ultima sezione prima del footer (mettilo penultimo o intermedio).\n"
    "Montalo davvero (attivazione su scroll), senza riscriverne la fisica."
)
FRAMER_HEADER = (
    "# VERIFIED ORIGINAL FRAMER INTERACTIVE\n\n"
    "**REGOLA D'ORO ZERO-DISTRUZIONE:** applica questa interazione DENTRO una sezione "
    "esistente compatibile. NON creare/cancellare/sostituire/fondere/riordinare sezioni. "
    "NON toccare il guest component già inserito. Montalo realmente (React portabile o "
    "runtime nativo), senza riscriverne fisica o struttura."
)


def build_prompts(result, arsenal_base, prompts_dir="prompts") -> list[str]:
    """Costruisce i 5 testi dei prompt combinando i fissi con la scelta della roulette.

    Args:
        result: RouletteResult (ha .component e .framers)
        arsenal_base: cartella arsenal (su Drive montato / VM)
        prompts_dir: cartella con i prompt fissi 01/02/05

    Returns:
        Lista di 5 stringhe (fasi 1..5), pronte per il sender.
    """
    arsenal = Path(arsenal_base)
    pdir = Path(prompts_dir)

    def fixed(name: str) -> str:
        f = pdir / name
        return f.read_text(encoding="utf-8") if f.exists() else ""

    phase1 = fixed("01_sito_da_reference.md")
    phase2 = fixed("02_animate_gsap.md")
    phase5 = fixed("05_correzione_finale.md")

    # fase 3: componente scelto dalla roulette
    if result.component:
        comp_dir = arsenal / "componenti" / result.component
        phase3 = assemble_component(comp_dir, COMPONENT_HEADER) if comp_dir.is_dir() \
            else f"{COMPONENT_HEADER}\n\nSelected: `{result.component}` (cartella non trovata)\n"
    else:
        phase3 = fixed("03_guest_component.md")

    # fase 4: primo framer scelto dalla roulette
    if result.framers:
        framer_dir = arsenal / "ANIMAZIONI" / "Framer_Interactions" / result.framers[0]
        phase4 = assemble_framer(framer_dir, FRAMER_HEADER) if framer_dir.is_dir() \
            else f"{FRAMER_HEADER}\n\nSelected: `{result.framers[0]}` (cartella non trovata)\n"
    else:
        phase4 = fixed("04_framer_interactive.md")

    return [phase1, phase2, phase3, phase4, phase5]
