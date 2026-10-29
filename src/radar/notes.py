"""Genera notas diarias en Markdown compatibles con Obsidian."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from radar.fetcher import Headline
from radar.sentiment import average_score, score_text


def build_daily_note(
    results: dict[str, list[Headline]],
    day: date | None = None,
) -> str:
    """Construye el markdown de la nota diaria con enlaces [[TICKER]]."""
    day = day or date.today()
    lines: list[str] = [
        f"# Radar de sentimiento — {day.isoformat()}",
        "",
        "> Solo menciones agregadas de fuentes públicas. "
        "Sin usernames, perfiles ni autores.",
        "",
        "## Resumen",
        "",
        "| Ticker | Titulares | Score promedio |",
        "|--------|-----------|----------------|",
    ]

    for ticker, headlines in sorted(results.items()):
        titles = [h.title for h in headlines]
        avg = average_score(titles)
        lines.append(f"| [[{ticker}]] | {len(headlines)} | {avg:+.2f} |")

    lines.extend(["", "## Detalle por ticker", ""])

    for ticker, headlines in sorted(results.items()):
        lines.append(f"### [[{ticker}]]")
        lines.append("")
        if not headlines:
            lines.append("_Sin titulares hoy._")
            lines.append("")
            continue
        for h in headlines:
            s = score_text(h.title)
            title_safe = h.title.replace("|", "/")
            link = f" — [fuente]({h.link})" if h.link else ""
            lines.append(f"- ({s.score:+.2f}) {title_safe}{link}")
        lines.append("")

    lines.extend(
        [
            "---",
            f"_Generado por radar-sentimiento el {day.isoformat()}_",
            "",
        ]
    )
    return "\n".join(lines)


def write_daily_note(
    results: dict[str, list[Headline]],
    output_dir: Path | str,
    day: date | None = None,
) -> Path:
    """Escribe la nota en output_dir/radar-YYYY-MM-DD.md."""
    day = day or date.today()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"radar-{day.isoformat()}.md"
    path.write_text(build_daily_note(results, day), encoding="utf-8")
    return path
