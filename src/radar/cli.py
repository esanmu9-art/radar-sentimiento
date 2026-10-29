"""CLI: python -m radar --tickers AAPL NVDA"""

from __future__ import annotations

import argparse
from pathlib import Path

from radar.config import load_config
from radar.fetcher import fetch_headlines_for_ticker
from radar.notes import write_daily_note
from radar.sentiment import average_score


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="radar",
        description="Radar de sentimiento agregado por ticker (RSS públicos).",
    )
    p.add_argument(
        "--tickers",
        nargs="+",
        help="Tickers a consultar (ej. AAPL NVDA). Por defecto usa config/watchlist.yaml.",
    )
    p.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Ruta al YAML de watchlist.",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Carpeta de salida para la nota Obsidian.",
    )
    p.add_argument(
        "--lang",
        nargs="+",
        default=None,
        help="Idiomas para Google News (ej. es en).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)

    tickers = [t.upper() for t in (args.tickers or cfg["tickers"])]
    languages = args.lang or cfg.get("languages", ["es", "en"])
    output_dir = args.output or Path(cfg.get("output_dir", "output"))

    print(f"Radar — tickers: {', '.join(tickers)}")
    print(f"Idiomas: {', '.join(languages)}")
    print()

    results = {}
    for ticker in tickers:
        print(f"Buscando {ticker}…")
        headlines = fetch_headlines_for_ticker(ticker, languages=languages)
        results[ticker] = headlines
        avg = average_score([h.title for h in headlines])
        print(f"  → {len(headlines)} titulares | score promedio: {avg:+.2f}")

    print()
    note_path = write_daily_note(results, output_dir)
    print(f"Nota Obsidian escrita en: {note_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
