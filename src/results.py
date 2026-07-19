"""Gestione della cartella dei risultati."""

from __future__ import annotations

from pathlib import Path

from .config import Config


def result_dir_for(job_name: str, cfg: Config) -> Path:
    """Cartella di destinazione del risultato per un job: results/<nome_job>/."""
    base = Path(cfg.get("result.output_dir", "./results"))
    dest = base / job_name
    dest.mkdir(parents=True, exist_ok=True)
    return dest
