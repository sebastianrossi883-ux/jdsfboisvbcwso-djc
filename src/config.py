"""Caricamento della configurazione da config.yaml (+ .env)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

try:
    from dotenv import load_dotenv
except ImportError:  # dotenv è opzionale
    load_dotenv = None

DEFAULT_CONFIG_PATH = "config.yaml"


def _deep_merge(base: dict, override: dict) -> dict:
    """Unisce due dizionari in profondità (override vince)."""
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


# Valori di default: così il programma parte anche con un config parziale.
DEFAULTS: dict[str, Any] = {
    "source": {
        "type": "local",
        "local": {"path": "./material"},
        "gdrive": {
            "folder_id": "",
            "credentials_file": "./gdrive-service-account.json",
            "download_dir": "./material",
        },
    },
    "stitch": {
        "url": "https://stitch.withgoogle.com/",
        "model": "3.1 pro",
        "version": "web",
        "headless": True,
        "user_data_dir": "./.stitch_profile",
        "slow_mo_ms": 50,
        "timeouts": {"navigation_ms": 60000, "generation_ms": 900000},
        "selectors": {},
    },
    "prompt": {
        "mode": "passthrough",
        "claude": {
            "model": "claude-opus-4-8",
            "max_tokens": 4000,
            "system": "",
        },
    },
    "result": {"type": "code", "output_dir": "./results"},
    "loop": {"poll_interval_sec": 60, "once": False},
}


class Config:
    """Wrapper leggero sul dizionario di configurazione con accesso a punti."""

    def __init__(self, data: dict[str, Any]):
        self._data = data

    def get(self, path: str, default: Any = None) -> Any:
        """Legge una chiave annidata, es. cfg.get('stitch.model')."""
        node: Any = self._data
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def data(self) -> dict[str, Any]:
        return self._data


def load_config(path: str | None = None) -> Config:
    """Carica .env e config.yaml, li fonde con i default e restituisce un Config."""
    if load_dotenv is not None:
        load_dotenv()

    config_path = path or os.environ.get("STITCH_BOT_CONFIG") or DEFAULT_CONFIG_PATH
    file_data: dict[str, Any] = {}
    if Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as fh:
            file_data = yaml.safe_load(fh) or {}
    else:
        raise FileNotFoundError(
            f"Config non trovato: {config_path}. "
            "Copia config.example.yaml in config.yaml e modificalo."
        )

    merged = _deep_merge(DEFAULTS, file_data)
    return Config(merged)
