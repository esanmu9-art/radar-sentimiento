"""Pruebas de la nota diaria Obsidian."""

from radar.fetcher import Headline
from radar.notes import build_daily_note


def test_note_contains_obsidian_links_and_privacy_line():
    results = {
        "AAPL": [
            Headline(
                ticker="AAPL",
                title="Apple stock surges on growth",
                link="https://example.com/a",
                published="",
                source="test",
            )
        ],
        "NVDA": [],
    }
    md = build_daily_note(results)
    assert "[[AAPL]]" in md
    assert "[[NVDA]]" in md
    assert "Sin usernames" in md
    assert "Radar de sentimiento" in md
