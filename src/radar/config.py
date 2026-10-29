"""Carga de configuración (watchlist y rutas)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "watchlist.yaml"


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    """Lee el YAML de watchlist. Si no existe, usa valores mínimos."""
    cfg_path = Path(path) if path else DEFAULT_CONFIG
    if not cfg_path.exists():
        return {
            "tickers": ["AAPL", "NVDA"],
            "languages": ["es", "en"],
            "output_dir": "output",
        }
    with cfg_path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    data.setdefault("tickers", ["AAPL", "NVDA"])
    data.setdefault("languages", ["es", "en"])
    data.setdefault("output_dir", "output")
    return data
