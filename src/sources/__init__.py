"""Sorgenti del materiale: locale o Google Drive.

Una sorgente sa:
  - elencare i job "pendenti" (da fare)
  - marcare un job come "fatto" o "in errore"
"""

from __future__ import annotations

from ..config import Config
from .base import Source
from .local import LocalSource


def build_source(cfg: Config) -> Source:
    """Factory: crea la sorgente giusta in base a config.source.type."""
    source_type = cfg.get("source.type", "local")

    if source_type == "local":
        return LocalSource(cfg)

    if source_type == "gdrive":
        # import ritardato: le dipendenze Google servono solo in questo caso
        from .gdrive import GDriveSource

        return GDriveSource(cfg)

    raise ValueError(f"source.type sconosciuto: {source_type!r} (usa 'local' o 'gdrive')")


__all__ = ["Source", "LocalSource", "build_source"]
