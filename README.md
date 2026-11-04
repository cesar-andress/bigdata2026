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

## Estado de los equipos (4 de noviembre de 2026)

Comprobado ese día contra la rama por defecto de cada GitHub, con
`pytest tests/hito1` y `pytest tests/hito2` de este repositorio.
**Pasar** significa cero fallos. Con un fallo, el hito no está cumplido.

El límite del Hito 1 es el **4 de noviembre de 2026**. El del Hito 2 es
el **11 de noviembre de 2026, a las 23:59**. A fecha de esta tabla,
**ningún equipo pasaría ninguno de los dos hitos.**

| Repositorio | Commit comprobado | Hito 1 | ¿Pasa el Hito 1? | Hito 2 | ¿Pasa el Hito 2? |
| --- | --- | --- | --- | --- | --- |
| [nasratullahjabarkhil/bigdata](https://github.com/nasratullahjabarkhil/bigdata) | `16f1941` · 28/10/2026 | 34 passed, 30 failed, 1 skipped | No | 0 passed, 20 failed | No |
| [edurlix/BigDataProject](https://github.com/edurlix/BigDataProject) | `dd59cee` · 28/10/2026 | 34 passed, 30 failed, 1 skipped | No | 0 passed, 20 failed | No |
| [rmmenendez05/dsbd-big-data-repo](https://github.com/rmmenendez05/dsbd-big-data-repo) | `ba06a3b` · 28/10/2026 | 33 passed, 30 failed, 2 skipped | No | 0 passed, 20 failed | No |
| [hracjc/dsbd_etl_1](https://github.com/hracjc/dsbd_etl_1) | `5430089` · 04/11/2026 15:45 | 33 passed, 31 failed, 1 skipped | No | 0 passed, 20 failed | No |
| [marcosgale/BigData_Proyecto](https://github.com/marcosgale/BigData_Proyecto) | `f18abfd` · 04/11/2026 12:53 | 45 passed, 19 failed, 1 skipped | No | 0 passed, 20 failed | No |
| [Sumitodemarmeto/Practica_02_BigData](https://github.com/Sumitodemarmeto/Practica_02_BigData) | sin commits en `origin` | no se puede ejecutar | No | no se puede ejecutar | No |

Lo que sí aguanta en los cinco repos con código es la ejecución de la
Práctica 1 (`pytest -m runtime`): 26 passed. Eso no cuenta como Hito 1.
El Hito 2 está a cero en todos: no hay `spark/job_01.py`, ni cierre, ni
etiqueta `entrega-02`.

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
