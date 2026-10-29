# Radar de sentimiento por ticker

Herramienta personal en Python que revisa **titulares públicos** (RSS) sobre acciones que te interesan, les pone un **score de sentimiento** muy simple y genera una **nota diaria en Markdown** lista para Obsidian (`[[AAPL]]`, etc.).

Proyecto propio, pensado para crecer con un asistente de IA (p. ej. en el programa de Alignerr). La base es deliberadamente mínima: lo que ves aquí funciona, y el resto del roadmap está para construirlo después.

## Principio de privacidad

- Solo se guardan **menciones agregadas** de tickers: título, enlace, fecha y nombre del feed.
- **Nunca** se almacenan usernames, perfiles, autores de posts ni datos personales de terceros.
- Fuentes actuales: Google News RSS y Yahoo Finance RSS (canales públicos).
- No hay scrapers de redes sociales con identidad de usuario, ni OSINT sobre personas.

## Qué hace ahora (v0.1)

1. Lee una watchlist en `config/watchlist.yaml`.
2. Descarga titulares RSS por ticker.
3. Puntúa cada título con un léxico corto ES/EN (placeholder).
4. Imprime conteo + score promedio en la terminal.
5. Escribe `output/radar-YYYY-MM-DD.md` con enlaces `[[TICKER]]` para Obsidian.

## Requisitos

- Python 3.10+
- Dependencias en `requirements.txt`

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
# Usa la watchlist de config/watchlist.yaml
python -m radar

# O pasa tickers a mano
python -m radar --tickers AAPL NVDA META

# Cambia carpeta de salida (p. ej. tu bóveda de Obsidian)
python -m radar --tickers AAPL --output "/ruta/a/tu/vault/Radar"
```

Ejemplo de salida:

```
Radar — tickers: AAPL, NVDA
Idiomas: es, en

Buscando AAPL…
  → 28 titulares | score promedio: +0.12
Buscando NVDA…
  → 31 titulares | score promedio: +0.08

Nota Obsidian escrita en: output/radar-2026-10-27.md
```

## Roadmap (para construir después)

Marca lo que vayas completando:

- [ ] Más fuentes RSS de noticias financieras (Bloomberg, Reuters, Expansión, etc.)
- [ ] Conteos agregados de menciones en Reddit (solo totales por ticker, **sin** usernames)
- [ ] Score de sentimiento más serio (VADER, TextBlob o un clasificador propio — no entrenar modelos grandes aquí)
- [ ] Alertas cuando el score o el volumen de menciones se dispara
- [ ] Exportar la nota diaria **directo** a una carpeta de tu vault de Obsidian
- [ ] Export CSV para comparar con backtests / estrategias de TradingView (Pine)
- [ ] Gráficos simples (matplotlib) de score diario por ticker
- [ ] Historial local (SQLite) de scores agregados día a día
- [ ] Integración opcional con tus scripts de Pine / Market Diem (solo tickers y precios públicos)

## Estructura

```
radar-sentimiento/
├── config/watchlist.yaml      # tus tickers
├── src/radar/
│   ├── cli.py                 # entrada: python -m radar
│   ├── config.py
│   ├── fetcher.py             # RSS públicos
│   ├── sentiment.py           # léxico placeholder
│   └── notes.py               # markdown Obsidian
├── tests/
├── output/                    # notas generadas (gitignoradas)
├── requirements.txt
├── pyproject.toml
└── LICENSE                    # pon tu nombre en el copyright
```

## Pruebas

```bash
pip install pytest
pytest
```

## Licencia

MIT — edita `LICENSE` y sustituye `TU NOMBRE` por el tuyo antes del primer commit.

## Aviso

Esto **no** es consejo de inversión. Es una herramienta personal de investigación sobre información pública agregada.
