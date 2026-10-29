"""Pruebas del puntuador léxico (placeholder)."""

from radar.sentiment import average_score, score_text


def test_positive_english_headline():
    result = score_text("Apple stock surges after strong growth and profit beat")
    assert result.positives >= 2
    assert result.score > 0


def test_negative_spanish_headline():
    result = score_text("La acción cae tras pérdidas y un recorte bajista")
    assert result.negatives >= 2
    assert result.score < 0


def test_neutral_and_average():
    assert score_text("La empresa presentó su reporte trimestral").score == 0.0
    assert average_score([]) == 0.0
    avg = average_score(
        [
            "NVDA rallies on record gains",
            "TSLA plunges after losses",
        ]
    )
    # uno positivo, uno negativo → cerca de 0
    assert -0.5 <= avg <= 0.5
