"""Puntuador de sentimiento léxico — placeholder deliberadamente simple.

No es un modelo de ML. Es una lista corta de palabras positivas/negativas
en español e inglés para arrancar. Sustitúyelo después por algo mejor
(VADER, TextBlob, o un clasificador propio) durante las sesiones de Alignerr.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Listas mínimas a propósito. Amplíalas o cámbialas por un scorer real.
POSITIVE = {
    # EN
    "gain",
    "gains",
    "surge",
    "surges",
    "rally",
    "rallies",
    "beat",
    "beats",
    "record",
    "growth",
    "upgrade",
    "upgrades",
    "bullish",
    "profit",
    "profits",
    "strong",
    "soar",
    "soars",
    "rise",
    "rises",
    "jump",
    "jumps",
    "outperform",
    # ES
    "sube",
    "suben",
    "alza",
    "ganancia",
    "ganancias",
    "récord",
    "record",
    "crecimiento",
    "mejora",
    "mejoran",
    "alcista",
    "beneficio",
    "beneficios",
    "fuerte",
    "impulso",
    "rompe",
    "superan",
    "supera",
}

NEGATIVE = {
    # EN
    "fall",
    "falls",
    "drop",
    "drops",
    "loss",
    "losses",
    "miss",
    "misses",
    "cut",
    "cuts",
    "downgrade",
    "downgrades",
    "bearish",
    "weak",
    "crash",
    "crashes",
    "plunge",
    "plunges",
    "decline",
    "declines",
    "lawsuit",
    "probe",
    "fraud",
    # ES
    "cae",
    "caen",
    "baja",
    "bajan",
    "pérdida",
    "perdida",
    "pérdidas",
    "perdidas",
    "corte",
    "recorta",
    "recortes",
    "bajista",
    "débil",
    "debil",
    "desplome",
    "demanda",
    "fraude",
    "investigación",
    "investigacion",
    "riesgo",
}

_TOKEN = re.compile(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+")


@dataclass
class SentimentResult:
    score: float  # -1.0 … +1.0
    positives: int
    negatives: int
    tokens: int


def score_text(text: str) -> SentimentResult:
    """Puntúa un texto con conteo léxico simple.

    score = (pos - neg) / max(pos + neg, 1), acotado a [-1, 1].
    Si no hay palabras de la lista, score = 0.0.
    """
    tokens = [t.casefold() for t in _TOKEN.findall(text or "")]
    pos = sum(1 for t in tokens if t in POSITIVE)
    neg = sum(1 for t in tokens if t in NEGATIVE)
    total = pos + neg
    if total == 0:
        score = 0.0
    else:
        score = (pos - neg) / total
    return SentimentResult(score=score, positives=pos, negatives=neg, tokens=len(tokens))


def average_score(texts: list[str]) -> float:
    """Promedio de scores; 0.0 si la lista está vacía."""
    if not texts:
        return 0.0
    return sum(score_text(t).score for t in texts) / len(texts)
