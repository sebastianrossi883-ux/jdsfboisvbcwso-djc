"""Splitter di reference — porting fedele del tuo `split_references.py`.

Divide ogni reference-immagine in N fette verticali (default 3), dall'alto in
basso, con un piccolo overlap del 2% ai bordi (così non si tagliano righe).
La HERO sta sempre nella `parte-1` (il top dello screenshot).

Struttura prodotta (identica all'originale):
    <outDir>/<nome-reference-slug>/parte-1-di-3.png
                                   parte-2-di-3.png
                                   parte-3-di-3.png
    <outDir>/INDICE_SPLIT.md

Come l'originale, processa SOLO i file immagine direttamente dentro la cartella
sorgente: le eventuali sottocartelle (es. "ALTRE REFERENCE") sono escluse.

Uso da riga di comando (stessa firma dell'originale):
    python -m src.reference_splitter [srcDir] [outDir] [N]
    # esempio: due reference in material/REFENCE -> fette in material/references_split
    python -m src.reference_splitter material/REFENCE material/references_split 3

Uso da codice:
    from src.reference_splitter import split_references, split_image
    result = split_references("material/REFENCE", "material/references_split", parts=3)
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

from PIL import Image

log = logging.getLogger(__name__)

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_OVERLAP = 0.02  # 2% ai bordi, come nell'originale


def slug(name: str) -> str:
    """Trasforma un nome file in uno slug pulito (come nell'originale)."""
    s = re.sub(r"\.(png|jpe?g|webp)$", "", name, flags=re.I)
    s = re.sub(r"[^a-z0-9]+", "-", s, flags=re.I).strip("-").lower()
    return s[:60] or "ref"


def split_image(
    src: str | Path,
    out_dir: str | Path,
    parts: int = 3,
    overlap: float = DEFAULT_OVERLAP,
    name: str | None = None,
    compress_level: int = 1,
) -> list[Path]:
    """Divide UNA immagine in `parts` fette verticali in `out_dir/<slug>/`.

    Returns:
        La lista dei percorsi delle fette create (parte-1, parte-2, ...).
    """
    parts = max(2, int(parts))
    src = Path(src)
    img = Image.open(src).convert("RGB")
    width, height = img.size

    band = -(-height // parts)          # ceil(height / parts)
    ov = round(height * overlap)         # overlap in pixel

    name = name or slug(src.name)
    sub = Path(out_dir) / name
    sub.mkdir(parents=True, exist_ok=True)

    # pulisci eventuali fette vecchie
    for old in sub.glob("parte-*.png"):
        old.unlink()

    outputs: list[Path] = []
    for i in range(parts):
        y0 = max(0, i * band - (ov if i > 0 else 0))
        y1 = min(height, (i + 1) * band + (ov if i < parts - 1 else 0))
        crop = img.crop((0, y0, width, y1))
        out_path = sub / f"parte-{i + 1}-di-{parts}.png"
        crop.save(out_path, compress_level=compress_level)
        outputs.append(out_path)

    log.info("ok %s (%dx%d, %d pezzi)", name, width, height, parts)
    return outputs


def split_references(
    src: str | Path,
    out_dir: str | Path,
    parts: int = 3,
    overlap: float = DEFAULT_OVERLAP,
    write_index: bool = True,
) -> dict[str, list[Path]]:
    """Divide tutte le immagini top-level di `src` (sottocartelle escluse).

    Scrive anche un INDICE_SPLIT.md, come l'originale.

    Returns:
        Dizionario {slug_reference: [fette...]}.
    """
    src = Path(src)
    out_dir = Path(out_dir)
    if not src.is_dir():
        raise NotADirectoryError(f"Cartella sorgente non trovata: {src}")

    # SOLO file diretti: le sottocartelle (es. "ALTRE REFERENCE") sono escluse
    files = sorted(
        p for p in src.iterdir()
        if p.is_file() and p.suffix.lower() in IMG_EXT
    )
    if not files:
        raise FileNotFoundError(f"Nessuna immagine in {src}")

    out_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[Path]] = {}
    index_lines: list[str] = []
    skipped = 0

    for p in files:
        try:
            img = Image.open(p)
            w, h = img.size
        except Exception as exc:  # noqa: BLE001
            log.warning("[skip] %s: %s", p.name, exc)
            skipped += 1
            continue
        name = slug(p.name)
        results[name] = split_image(p, out_dir, parts=parts, overlap=overlap, name=name)
        index_lines.append(
            f"- **{name}** ({w}x{h}, {parts} pezzi) - hero = parte-1 - da `{src.name}/{p.name}`"
        )

    if write_index:
        index = (
            f"# Reference pre-divise ({len(results)}) - per la HERO shape\n\n"
            f"Ogni reference ha una sottocartella con {parts} pezzi. "
            f"La HERO e nel **parte-1** (il top).\n"
            f"Usane UNA sola, opposta alla hero del sorgente. Mai copiarne palette/foto/testi.\n"
            f"Le sottocartelle della sorgente sono ESCLUSE da questo export.\n\n"
            + "\n".join(index_lines) + "\n"
        )
        (out_dir / "INDICE_SPLIT.md").write_text(index, encoding="utf-8")

    log.info("FATTO: %d reference divise (%d saltate) in %s", len(results), skipped, out_dir)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Divide le reference di una cartella in N fette verticali."
    )
    parser.add_argument("srcDir", nargs="?", default="material/REFENCE",
                        help="Cartella con le reference (default: material/REFENCE)")
    parser.add_argument("outDir", nargs="?", default="material/references_split",
                        help="Cartella di destinazione (default: material/references_split)")
    parser.add_argument("N", nargs="?", type=int, default=3,
                        help="In quante parti dividere ogni reference (default 3, min 2)")
    parser.add_argument("--overlap", type=float, default=DEFAULT_OVERLAP,
                        help="Overlap ai bordi in frazione (default 0.02 = 2%%)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    results = split_references(args.srcDir, args.outDir, parts=args.N, overlap=args.overlap)

    total = sum(len(v) for v in results.values())
    print(f"\nFATTO: {len(results)} reference -> {total} fette totali in {args.outDir}")
    print(f"Indice: {Path(args.outDir) / 'INDICE_SPLIT.md'}")


if __name__ == "__main__":
    main()
