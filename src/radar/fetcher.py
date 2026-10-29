"""Fetcher de titulares públicos vía RSS (sin datos personales).

Solo guarda título, enlace, fecha y fuente agregada.
Nunca guarda autores, usernames ni perfiles.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import quote_plus

import feedparser
import requests

USER_AGENT = "radar-sentimiento/0.1 (+https://github.com/example/radar-sentimiento; research)"


@dataclass
class Headline:
    """Titular agregado. Sin autor ni datos personales."""

    ticker: str
    title: str
    link: str
    published: str  # ISO o vacío
    source: str  # nombre del feed, no persona


def google_news_rss_url(ticker: str, lang: str = "en") -> str:
    """URL de búsqueda RSS de Google News para un ticker."""
    # hl/gl orientan el idioma; la query es el símbolo bursátil.
    query = quote_plus(f"{ticker} stock OR acciones")
    if lang.startswith("es"):
        return (
            f"https://news.google.com/rss/search?q={query}"
            f"&hl=es-419&gl=MX&ceid=MX:es-419"
        )
    return (
        f"https://news.google.com/rss/search?q={query}"
        f"&hl=en-US&gl=US&ceid=US:en"
    )


def yahoo_finance_rss_url(ticker: str) -> str:
    """Feed RSS de Yahoo Finance para un ticker (titulares de la compañía)."""
    return f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={quote_plus(ticker)}&region=US&lang=en-US"


def _parse_entries(ticker: str, feed: feedparser.FeedParserDict, source_label: str) -> list[Headline]:
    headlines: list[Headline] = []
    for entry in feed.entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not title:
            continue
        published = ""
        if entry.get("published_parsed"):
            try:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
            except (TypeError, ValueError):
                published = str(entry.get("published") or "")
        elif entry.get("published"):
            published = str(entry.published)
        # feed.feed.get("title") es el nombre del canal, no de una persona
        source = source_label
        headlines.append(
            Headline(
                ticker=ticker.upper(),
                title=title,
                link=link,
                published=published,
                source=source,
            )
        )
    return headlines


def fetch_rss(url: str, timeout: float = 20.0) -> feedparser.FeedParserDict:
    """Descarga un feed RSS con User-Agent explícito."""
    resp = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return feedparser.parse(resp.content)


def fetch_headlines_for_ticker(
    ticker: str,
    languages: Iterable[str] | None = None,
    max_per_source: int = 15,
) -> list[Headline]:
    """Obtiene titulares públicos agregados para un ticker.

    Fuentes:
    - Google News RSS (por idioma)
    - Yahoo Finance RSS
    """
    langs = list(languages) if languages else ["en"]
    collected: list[Headline] = []
    seen_titles: set[str] = set()

    urls: list[tuple[str, str]] = []
    for lang in langs:
        urls.append((google_news_rss_url(ticker, lang), f"google-news-{lang}"))
    urls.append((yahoo_finance_rss_url(ticker), "yahoo-finance"))

    for url, label in urls:
        try:
            feed = fetch_rss(url)
        except Exception as exc:  # red cae → seguimos con otras fuentes
            print(f"  [aviso] no se pudo leer {label} para {ticker}: {exc}")
            continue
        for h in _parse_entries(ticker, feed, label)[:max_per_source]:
            key = h.title.casefold()
            if key in seen_titles:
                continue
            seen_titles.add(key)
            collected.append(h)

    return collected
