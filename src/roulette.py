"""Roulette degli ingredienti (porting fedele di super_roulette.cjs).

Ad ogni giro pesca a caso dagli arsenali, MA senza ripetere: tiene una memoria
permanente (`roulette_history.json`) e quando una categoria è esaurita la resetta
e ricomincia. Così passa per TUTTO l'arsenal prima di ripetere qualcosa.

Pesca:
  - 1 sito reference (guida il design)
  - 1 design DNA (mood/filosofia)
  - 1 guest component  -> PREFERISCE le versioni React, esclude webgl/three/shader
  - 3 effetti Framer
  - 2 plugin GSAP (+ SplitText sempre)
  - 2 font (display + body)

L'arsenal vive su disco (in locale, o su Drive montato in Colab): i percorsi
sono in config, sezione `roulette`.
"""

from __future__ import annotations

import json
import logging
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger(__name__)

# formati/temi esclusi dai guest component (come nell'originale)
COMPONENT_EXCLUDE = ("three", "webgl", "shader")
# plugin GSAP "interessanti" (come nell'originale)
GSAP_INTERESTING = [
    "Flip.js", "DrawSVGPlugin.js", "MorphSVGPlugin.js", "ScrambleTextPlugin.js",
    "InertiaPlugin.js", "Observer.js", "ScrollSmoother.js",
]
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}


@dataclass
class RouletteConfig:
    base: Path
    siti_dir: str = "SITI SCARICATI"
    dna_dir: str = "DESIGN MD"
    componenti_dir: str = "componenti"
    animazioni_dir: str = "ANIMAZIONI"
    font_dir: str = "FONT "
    framer_subdir: str = "Framer_Interactions"
    gsap_subdir: str = "gsap-public/esm"
    history_file: str = "roulette_history.json"
    prefer_react_components: bool = True

    def p(self, *parts: str) -> Path:
        return self.base.joinpath(*parts)


@dataclass
class RouletteResult:
    sito: str | None = None
    dna: str | None = None
    component: str | None = None
    framers: list[str] = field(default_factory=list)
    gsap_plugins: list[str] = field(default_factory=list)
    font_display: str | None = None
    font_body: str | None = None

    def as_dict(self) -> dict:
        return {
            "sito": self.sito,
            "dna": self.dna,
            "component": self.component,
            "framers": self.framers,
            "gsap_plugins": self.gsap_plugins,
            "font_display": self.font_display,
            "font_body": self.font_body,
        }


# ---- memoria ---------------------------------------------------------------

_DEFAULT_HISTORY = {
    "SITI": [], "DNA": [], "COMPONENTI_REACT": [], "FRAMER": [], "GSAP": [], "FONT": [],
}


def load_history(path: Path) -> dict:
    if path.exists():
        try:
            return {**_DEFAULT_HISTORY, **json.loads(path.read_text(encoding="utf-8"))}
        except Exception as exc:  # noqa: BLE001
            log.warning("Storico illeggibile (%s): riparto da zero.", exc)
    return {k: list(v) for k, v in _DEFAULT_HISTORY.items()}


def save_history(path: Path, history: dict) -> None:
    path.write_text(json.dumps(history, indent=2), encoding="utf-8")


# ---- utilità di scelta (memoria anti-ripetizione) --------------------------

def _get_dirs(folder: Path) -> list[str]:
    if not folder.is_dir():
        return []
    out = []
    for item in sorted(folder.iterdir()):
        if item.name.startswith(".") or item.name == "__MACOSX":
            continue
        if item.is_dir():
            out.append(item.name)
    return out


def pick_unique(items: list[str], history_list: list[str], exclude: list[str] | None = None) -> str | None:
    """Pesca un item non ancora usato; se esauriti, RESETTA la memoria e ricomincia."""
    exclude = exclude or []
    if not items:
        return None
    available = [i for i in items if i not in history_list and i not in exclude]
    if not available:
        log.info("Categoria esaurita: resetto la memoria e ricomincio.")
        history_list.clear()
        available = [i for i in items if i not in exclude] or list(items)
    choice = random.choice(available)
    if choice not in history_list:
        history_list.append(choice)
    return choice


def pick_many(items: list[str], history_list: list[str], n: int) -> list[str]:
    out: list[str] = []
    for _ in range(n):
        pick = pick_unique(items, history_list, exclude=out)
        if pick is None:
            break
        out.append(pick)
    return out


# ---- selezione componenti (preferisce React, esclude webgl/three/shader) ---

def _is_react_component(folder: Path) -> bool:
    """True se la cartella contiene sorgenti React (.tsx/.jsx) o ha nome *React."""
    if folder.name.lower().endswith("react"):
        return True
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".tsx", ".jsx"):
            return True
    return False


def _eligible_components(componenti: Path, prefer_react: bool) -> list[str]:
    names = _get_dirs(componenti)
    # escludi webgl/three/shader
    names = [n for n in names if not any(x in n.lower() for x in COMPONENT_EXCLUDE)]
    if prefer_react:
        react = [n for n in names if _is_react_component(componenti / n)]
        if react:
            return react
    return names


# ---- API principale --------------------------------------------------------

def spin(cfg: RouletteConfig) -> RouletteResult:
    """Esegue un giro completo di roulette e aggiorna la memoria permanente."""
    hist_path = cfg.p(cfg.history_file)
    history = load_history(hist_path)
    result = RouletteResult()

    # 1) sito reference
    siti = _get_dirs(cfg.p(cfg.siti_dir))
    result.sito = pick_unique(siti, history["SITI"])

    # 2) design DNA (file .md nelle sottocartelle di DESIGN MD)
    dna_items: list[str] = []
    dna_root = cfg.p(cfg.dna_dir)
    if dna_root.is_dir():
        for item in sorted(dna_root.iterdir()):
            if item.name.startswith(".") or item.name == "__MACOSX":
                continue
            if item.is_dir():
                for f in sorted(item.iterdir()):
                    if f.suffix.lower() == ".md" and "index" not in f.name.lower():
                        dna_items.append(f"{item.name}/{f.name}")
            elif item.suffix.lower() == ".md" and "index" not in item.name.lower():
                dna_items.append(item.name)
    result.dna = pick_unique(dna_items, history["DNA"])

    # 3) guest component (React preferito, no webgl/three/shader)
    components = _eligible_components(cfg.p(cfg.componenti_dir), cfg.prefer_react_components)
    result.component = pick_unique(components, history["COMPONENTI_REACT"])

    # 4a) 3 effetti Framer
    framer_dir = cfg.p(cfg.animazioni_dir, cfg.framer_subdir)
    framers = [f for f in _get_dirs(framer_dir) if f != cfg.framer_subdir]
    result.framers = pick_many(framers, history["FRAMER"], 3)

    # 4b) 2 plugin GSAP premium (+ SplitText sempre)
    gsap_dir = cfg.p(cfg.animazioni_dir, cfg.gsap_subdir)
    gsap_all = [p.name for p in gsap_dir.iterdir()] if gsap_dir.is_dir() else []
    gsap_pool = [p for p in GSAP_INTERESTING if p in gsap_all]
    result.gsap_plugins = ["SplitText.js"] + pick_many(gsap_pool, history["GSAP"], 2)

    # 5) 2 font (display + body)
    fonts: list[str] = []
    font_parents = _get_dirs(cfg.p(cfg.font_dir))
    if font_parents:
        font_root = cfg.p(cfg.font_dir, font_parents[0])
        fonts = [f for f in _get_dirs(font_root) if f.lower() != "static"]
    result.font_display = pick_unique(fonts, history["FONT"])
    body_pool = [f for f in fonts if f != result.font_display]
    result.font_body = pick_unique(body_pool, history["FONT"])

    save_history(hist_path, history)
    log.info("Roulette: sito=%s | component=%s | framer=%s | gsap=%s | font=%s+%s",
             result.sito, result.component, result.framers,
             result.gsap_plugins, result.font_display, result.font_body)
    return result


def config_from(cfg) -> RouletteConfig:
    """Costruisce una RouletteConfig dalla config globale (sezione `roulette`)."""
    return RouletteConfig(
        base=Path(cfg.get("roulette.arsenal_base", "./arsenal")),
        siti_dir=cfg.get("roulette.siti_dir", "SITI SCARICATI"),
        dna_dir=cfg.get("roulette.dna_dir", "DESIGN MD"),
        componenti_dir=cfg.get("roulette.componenti_dir", "componenti"),
        animazioni_dir=cfg.get("roulette.animazioni_dir", "ANIMAZIONI"),
        font_dir=cfg.get("roulette.font_dir", "FONT "),
        framer_subdir=cfg.get("roulette.framer_subdir", "Framer_Interactions"),
        gsap_subdir=cfg.get("roulette.gsap_subdir", "gsap-public/esm"),
        history_file=cfg.get("roulette.history_file", "roulette_history.json"),
        prefer_react_components=bool(cfg.get("roulette.prefer_react_components", True)),
    )


def main() -> None:
    """CLI: fa un giro di roulette e stampa la selezione. `python -m src.roulette`"""
    import json as _json

    from .config import load_config

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    cfg = load_config()
    result = spin(config_from(cfg))
    print(_json.dumps(result.as_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
