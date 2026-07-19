"""Costruzione della sequenza di prompt da inviare a Stitch.

Ogni job produce una lista di "passi" (PromptStep). Il primo passo porta con sé
le immagini reference; i passi successivi sono solo testo (i prompt in sequenza,
es. base -> animazioni), esattamente come nel flusso manuale su Stitch.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config
from .job import Job

log = logging.getLogger(__name__)


@dataclass
class PromptStep:
    """Un singolo invio su Stitch: testo + eventuali immagini da allegare."""

    text: str
    images: list[Path] = field(default_factory=list)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_steps(job: Job, cfg: Config) -> list[PromptStep]:
    """Trasforma un Job in una sequenza di PromptStep pronti per l'invio."""
    if not job.prompts:
        return []

    steps: list[PromptStep] = []
    for index, prompt_path in enumerate(job.prompts):
        text = _read_text(prompt_path)
        # Solo il PRIMO prompt porta le reference (come nel flusso reale).
        images = job.references if index == 0 else []
        steps.append(PromptStep(text=text, images=list(images)))

    if cfg.get("prompt.mode") == "claude":
        steps = _enhance_with_claude(steps, cfg)

    return steps


def _enhance_with_claude(steps: list[PromptStep], cfg: Config) -> list[PromptStep]:
    """Fa rielaborare i testi a Claude (opzionale). In caso di errore, passthrough."""
    try:
        import os

        from anthropic import Anthropic
    except ImportError:
        log.warning("anthropic non installato: uso i prompt originali (passthrough).")
        return steps

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.warning("ANTHROPIC_API_KEY assente: uso i prompt originali (passthrough).")
        return steps

    client = Anthropic(api_key=api_key)
    model = cfg.get("prompt.claude.model", "claude-opus-4-8")
    max_tokens = cfg.get("prompt.claude.max_tokens", 4000)
    system = cfg.get("prompt.claude.system", "")

    enhanced: list[PromptStep] = []
    for step in steps:
        try:
            message = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system or None,
                messages=[{"role": "user", "content": step.text}],
            )
            new_text = "".join(
                block.text for block in message.content if block.type == "text"
            ).strip()
            enhanced.append(PromptStep(text=new_text or step.text, images=step.images))
        except Exception as exc:  # noqa: BLE001 - non vogliamo fermare il loop
            log.warning("Rielaborazione Claude fallita (%s): uso il testo originale.", exc)
            enhanced.append(step)

    return enhanced
