"""Interfaccia comune delle sorgenti di materiale."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..job import Job


class Source(ABC):
    """Contratto che ogni sorgente (locale, Drive, ...) deve rispettare."""

    @abstractmethod
    def list_pending_jobs(self) -> list[Job]:
        """Restituisce i job ancora da elaborare."""

    @abstractmethod
    def mark_done(self, job: Job) -> None:
        """Segna un job come completato (non verrà rielaborato)."""

    @abstractmethod
    def mark_error(self, job: Job, error: str) -> None:
        """Segna un job come fallito, salvando il motivo."""
