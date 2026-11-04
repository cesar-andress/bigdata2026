# bigdata2026 — repositorio docente (DSBD)

Repositorio de **demostración del profesor** para el bloque Big Data
(curso 2026/27). Contiene:

1. El **código de la primera entrega** (starter ETL `raw → clean → serving`),
   sin solución del Hito 1 / T2.
2. La batería de **tests** del Hito 1 (`tests/hito1/`) y del Hito 2
   (`tests/hito2/`), sobre el contrato de la Entrega 2.
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

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q tests/hito1          # Hito 1
pytest -q tests/hito2          # Hito 2
pytest -q -m runtime           # solo lo que el código de la práctica 1 ya debe ejecutar
```

Sobre el starter original **los tests de contrato fallan a propósito**.
El Hito 1 mira extract a escala, idempotencia, transform tipado, Parquet
Hive, fichas y `CONTRIBUTORS.md`. El Hito 2 mira `spark/job_01.py`,
la coincidencia RDD / DataFrame / SQL / SQLite, `BUGS.md`,
`ENTREGA_02.md`, `evidencias/` y la etiqueta `entrega-02`.

Los marcados `runtime` ejecutan `src/` con datos mínimos y sin red. Tienen
que pasar también sobre el código de la Práctica 1, antes de cumplir el
Hito 1.

Para lanzar la misma batería contra otro clon, sin copiar `tests/` dentro:

```bash
pytest -q --repo=/ruta/al/clon
# o
DSBD_REPO=/ruta/al/clon pytest -q
```

El igual en `--repo=` importa: si la ruta va como argumento suelto, pytest
la toma por un directorio de tests.

## GitHub Actions

El workflow `Hitos 1 y 2 — comprobaciones` instala dependencias y lanza
`pytest` en Ubuntu, primero el Hito 1 y después el Hito 2. En la pestaña
**Actions** del repositorio podéis ver la ejecución automática tras cada push.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `src/` | Extract / transform / load / fichas |
| `sources.yaml` | Fuentes y países foco |
| `data/` | `raw` → `clean` → `serving` (artefactos locales, no versionados) |
| `tests/hito1/` | Comprobaciones del Hito 1, más la ejecución del ETL actual |
| `tests/hito2/` | Comprobaciones del Hito 2 (Spark y cierre) |
| `.github/workflows/` | CI con pytest |

## Reglas del framework (no romper)

- **Extract** no limpia ni une fuentes.
- **Transform** no descarga; solo lee `data/raw/`.
- **Load / fichas** no leen JSON bruto; solo `clean/` → `serving/`.
