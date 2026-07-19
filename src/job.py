"""Modello di un "job": una cartella con reference (immagini) + prompt (.md).

Un job può descriversi tramite un file `job.yaml` opzionale. Se manca, il job
viene dedotto automaticamente dal contenuto della cartella:

    <cartella_job>/
        job.yaml            (opzionale)
        *.jpg / *.png       -> reference (immagini da allegare)
        01_....md           -> prompt #1
        02_....md           -> prompt #2   (inviati in ordine alfabetico)
        ...

Il file `job.yaml` (se presente) permette di controllare esattamente ordine e
contenuti:

    name: cantina_artisan_heritage
    model: "3.1 pro"        # override opzionale del modello
    version: web            # override opzionale (web/app)
    references:             # elenco esplicito delle immagini (percorsi relativi)
      - refs/mauro_a1.jpg
      - refs/mauro_a2.jpg
    prompts:                # elenco esplicito dei .md, nell'ordine di invio
      - 01_design_system.md
      - 02_inventario.md
      - 03_motion_manifest.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
PROMPT_EXTENSIONS = {".md", ".txt"}
JOB_MANIFEST = "job.yaml"


@dataclass
class Job:
    """Un'unità di lavoro da inviare a Stitch."""

    name: str
    path: Path
    references: list[Path] = field(default_factory=list)
    prompts: list[Path] = field(default_factory=list)
    model: str | None = None
    version: str | None = None

    def is_valid(self) -> bool:
        """Un job è valido se ha almeno un prompt."""
        return len(self.prompts) > 0


def _collect_images(folder: Path) -> list[Path]:
    """Trova tutte le immagini in una cartella (ricorsivo), ordinate per nome."""
    images = [
        p for p in sorted(folder.rglob("*"))
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return images


def _collect_prompts(folder: Path) -> list[Path]:
    """Trova i file di prompt nella cartella (non ricorsivo), ordinati per nome."""
    prompts = [
        p for p in sorted(folder.iterdir())
        if p.is_file() and p.suffix.lower() in PROMPT_EXTENSIONS
    ]
    return prompts


def load_job(folder: Path) -> Job:
    """Costruisce un Job da una cartella, usando job.yaml se presente."""
    folder = Path(folder)
    manifest_path = folder / JOB_MANIFEST

    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = yaml.safe_load(fh) or {}

        name = manifest.get("name", folder.name)
        references = [folder / r for r in manifest.get("references", [])]
        prompts = [folder / p for p in manifest.get("prompts", [])]

        # Se il manifest non elenca reference/prompt, li deduciamo dalla cartella.
        if not references:
            references = _collect_images(folder)
        if not prompts:
            prompts = _collect_prompts(folder)

        return Job(
            name=name,
            path=folder,
            references=references,
            prompts=prompts,
            model=manifest.get("model"),
            version=manifest.get("version"),
        )

    # Nessun manifest: deduzione automatica.
    return Job(
        name=folder.name,
        path=folder,
        references=_collect_images(folder),
        prompts=_collect_prompts(folder),
    )
