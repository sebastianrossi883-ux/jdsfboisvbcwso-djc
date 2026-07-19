"""Automazione del sito Stitch tramite browser (Playwright)."""

from .sender import ModelDowngradeError, StitchSender

__all__ = ["StitchSender", "ModelDowngradeError"]
