# bigdata2026 — repositorio docente (DSBD)

Repositorio de **demostración del profesor** para el bloque Big Data
(curso 2026/27). Contiene:

1. El **código de la primera entrega** (starter ETL `raw → clean → serving`),
   sin solución del Hito 1 / T2.
2. La batería de **tests** (`tests/hito1/`) que comprueban el contrato del
   extract a escala.
3. Un **workflow de GitHub Actions** (`.github/workflows/hito1-tests.yml`)
   que ejecuta `pytest` en cada push y pull request.

No es la solución de la práctica: es el punto de partida que ya conocéis,
más la maquinaria de comprobación y CI para que veáis cómo se monta.

## Arranque local del ETL

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
```

Pasos sueltos: `python -m src.extract` · `python -m src.transform` ·
`python -m src.load` · `python -m src.build_cards`.

Reutilizar descargas ya hechas:

```bash
python -m src.pipeline --skip-extract
```

## Tests del Hito 1

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

Sobre el starter original **varios tests fallan a propósito**: el extract
aún no cumple paginación, reintentos, idempotencia, manifiesto acumulativo,
cortesía de equipo ni la ampliación a ≥ 6 indicadores WDI. Eso es el
contrato que tenéis que satisfacer en vuestro repositorio.

## GitHub Actions

El workflow `Hito 1 — comprobaciones` instala dependencias y lanza
`pytest` en Ubuntu. En la pestaña **Actions** del repositorio podéis ver
la ejecución automática tras cada push.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `src/` | Extract / transform / load / fichas |
| `sources.yaml` | Fuentes y países foco |
| `data/` | `raw` → `clean` → `serving` (artefactos locales, no versionados) |
| `tests/hito1/` | Comprobaciones del Hito 1 |
| `.github/workflows/` | CI con pytest |

## Reglas del framework (no romper)

- **Extract** no limpia ni une fuentes.
- **Transform** no descarga; solo lee `data/raw/`.
- **Load / fichas** no leen JSON bruto; solo `clean/` → `serving/`.
