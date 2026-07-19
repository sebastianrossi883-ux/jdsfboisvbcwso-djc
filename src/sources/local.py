"""Sorgente locale: i job sono le sottocartelle di una cartella sul disco.

Lo stato di ogni job è tracciato con file "marcatore" dentro la sua cartella:
  - `.done`  -> job completato con successo
  - `.error` -> job fallito (contiene il messaggio di errore)

Così, se il programma si riavvia, non rifà i job già completati.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ..config import Config
from ..job import Job, load_job
from .base import Source

log = logging.getLogger(__name__)

DONE_MARKER = ".done"
ERROR_MARKER = ".error"


class LocalSource(Source):
    def __init__(self, cfg: Config):
        self.root = Path(cfg.get("source.local.path", "./material"))
        self.root.mkdir(parents=True, exist_ok=True)

    def _job_dirs(self) -> list[Path]:
        """Sottocartelle candidate a essere job (esclude quelle nascoste)."""
        return [
            p for p in sorted(self.root.iterdir())
            if p.is_dir() and not p.name.startswith(".")
        ]

    def list_pending_jobs(self) -> list[Job]:
        pending: list[Job] = []
        for folder in self._job_dirs():
            if (folder / DONE_MARKER).exists():
                continue
            if (folder / ERROR_MARKER).exists():
                continue  # un errore va risolto a mano (rimuovi .error per riprovare)

            job = load_job(folder)
            if not job.is_valid():
                log.warning("Job '%s' ignorato: nessun prompt (.md) trovato.", folder.name)
                continue
            pending.append(job)
        return pending

    def mark_done(self, job: Job) -> None:
        (job.path / DONE_MARKER).write_text("ok\n", encoding="utf-8")

    def mark_error(self, job: Job, error: str) -> None:
        (job.path / ERROR_MARKER).write_text(error + "\n", encoding="utf-8")
