# bigdata2026 — repositorio docente (DSBD)

Repositorio de **demostración del profesor** para el bloque Big Data
(curso 2026/27). Contiene:

1. El **código de la primera entrega** (starter ETL `raw → clean → serving`),
   sin solución del Hito 1 / T2.
2. La batería de **tests** del Hito 1 (`tests/hito1/`) y del Hito 2
   (`tests/hito2/`), sobre el contrato de la Entrega 2.
3. Dos **workflows de GitHub Actions**: `hito1-tests.yml` y
   `hito2-tests.yml`. Cada uno ejecuta su `pytest` en cada push y pull request.

No es la solución de la práctica: es el punto de partida que ya conocéis,
más la maquinaria de comprobación y CI para que veáis cómo se monta.
El trabajo se hace en **vuestro** repositorio de equipo, no en este.

## Qué tenéis que hacer

El código de este repo es el de la Práctica 1. La Entrega 2 lo amplía.
Los tests de `tests/hito1/` y `tests/hito2/` leen ese código y dicen si
el contrato está cumplido. Un solo fallo y el hito no pasa.

### Hito 1 · 4 de noviembre de 2026

En vuestro repo, sobre el mismo ETL (`src/`, `sources.yaml`):

1. **Extract a escala.** Al menos seis indicadores del Banco Mundial,
   con `NY.GDP.PCAP.CD` y `SP.POP.TOTL` fijos y la serie completa
   (no `mrnev=1` ni una petición por país del foco). Paginación que
   cuadre con el `total` de la API. Lo que no sea HTTP 200 no se guarda
   en `data/raw/`. Reintentos con espera ante 429, 5xx y timeouts; un
   404 no se reintenta. La segunda ejecución no vuelve a descargar lo
   que ya está bien, salvo `--force`. El manifiesto es acumulativo y
   cada fila lleva `run_id`. Como mucho cinco peticiones por segundo,
   con un `User-Agent` que identifique a vuestro equipo.
2. **Universo y transform tipado.** Criterio de país, `countries.parquet`,
   `languages.parquet` y `excluded_entities.csv`. Equivalencias de código
   en la configuración. Indicadores con el esquema del enunciado, `year`
   entero, nulo si falta el dato, y error si se repite
   `(iso3, indicator_id, year, source_id)`. Huérfanos en
   `join_orphans.csv` por fuente e indicador.
3. **Parquet Hive** en `data/clean/indicators/indicator_id=<id>/`.
   `pyarrow` (o `fastparquet`) declarado en `requirements.txt`.
4. **Fichas** regeneradas desde `clean/` → SQLite, una por país, con la
   mediana de la región en el mismo indicador y el mismo año.
5. **`CONTRIBUTORS.md`** en la raíz del repo: nombre, apellidos y correo
   institucional `@…ucjc.edu`.

`pytest -m runtime` solo comprueba que la Práctica 1 sigue pudiendo
ejecutarse. Eso no sustituye al Hito 1.

### Hito 2 · 11 de noviembre de 2026, 23:59

Además de lo anterior:

1. **`spark/job_01.py`**, arrancable con `python spark/job_01.py`.
   Lee `data/clean/indicators`, calcula la cobertura por indicador y
   década tres veces (RDD al estilo MapReduce, DataFrame y Spark SQL)
   y la compara con el SQLite de `serving/`. Si no coinciden, el proceso
   sale con código distinto de 0. Escribe
   `data/serving/spark/cobertura_decada/` en Parquet, imprime el plan
   físico y el número de particiones, y deja el event log en
   `logs/spark-events/`.
2. **Pieza B.** `ENTREGA_02.md` (predicción, resultado, decisiones,
   evidencia, las tres preguntas de teoría y pendientes) y `BUGS.md`
   con al menos tres defectos (reproducción, efecto y arreglo).
3. **Pieza C.** El event log copiado en `evidencias/`.
4. **`.gitignore`** con `data/`, `logs/` y `.venv/`.
5. **Etiqueta** `entrega-02` en el repositorio (`git tag -a entrega-02`
   y `git push origin entrega-02`). La fecha de esa etiqueta en GitHub
   es la marca de la entrega.

### Cómo comprobarlo en vuestro código

Desde un clon de **este** repositorio, sin copiar `tests/` al vuestro:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q tests/hito1 --repo=/ruta/a/vuestro/clon
pytest -q tests/hito2 --repo=/ruta/a/vuestro/clon
```

El igual de `--repo=` es obligatorio. Si la ruta va suelta, pytest la
confunde con un directorio de tests. También vale
`DSBD_REPO=/ruta/a/vuestro/clon pytest -q`.

Estos tests no llaman al Banco Mundial ni regeneran `data/` de verdad.
Los de contrato leen vuestro código y `sources.yaml`. Los marcados
`runtime` ejecutan el ETL con ficheros mínimos y la red simulada, en un
directorio temporal. La prueba de aula sigue siendo la del enunciado:
clon limpio, `python -m src.pipeline` dos veces y `python spark/job_01.py`.

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
El detalle de qué mira cada hito, y cómo lanzar la batería contra
vuestro clon, está en «Qué tenéis que hacer».

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
| [hracjc/dsbd_etl_1](https://github.com/hracjc/dsbd_etl_1) | `694c4ff` · 04/11/2026 19:04, repo regenerado | 33 passed, 31 failed, 1 skipped | No | 0 passed, 20 failed | No |
| [marcosgale/BigData_Proyecto](https://github.com/marcosgale/BigData_Proyecto) | `f18abfd` · 04/11/2026 12:53 | 45 passed, 19 failed, 1 skipped | No | 0 passed, 20 failed | No |
| [Sumitodemarmeto/Practica_02_BigData](https://github.com/Sumitodemarmeto/Practica_02_BigData) | sin commits en `origin` | no se puede ejecutar | No | no se puede ejecutar | No |

Lo que sí aguanta en los repos que siguen con el starter es la ejecución
de la Práctica 1 (`pytest -m runtime`): 26 passed. Eso no cuenta como
Hito 1. El Hito 2 está a cero en todos: no hay `spark/job_01.py`, ni
cierre, ni etiqueta `entrega-02`.

[hracjc/dsbd_etl_1](https://github.com/hracjc/dsbd_etl_1) se borró y se
volvió a crear. El `main` nuevo es `694c4ff` (4 de noviembre de 2026,
19:04). Tiene las etiquetas `1.0.0` y `1.0.1`, no `entrega-02`. Copió
los dos workflows y `tests/`, pero no el `conftest.py` de la raíz ni
`pytest.ini`. Sus Actions no llegan a evaluar el código: los 65 tests
del Hito 1 y los 20 del Hito 2 terminan en error (`no option named
'--repo'`). Medidos desde este repositorio, tampoco pasan. Además,
`load_config` abre `country_list.csv` con una ruta relativa al
directorio de trabajo, y el extract nuevo exige `raise_for_status` en
la respuesta: tres tests de `runtime` fallan por eso.

## Cómo funcionan las tareas automatizadas

Hay dos workflows de **GitHub Actions**, uno por hito:

- `.github/workflows/hito1-tests.yml` ejecuta `pytest -q tests/hito1`.
- `.github/workflows/hito2-tests.yml` ejecuta `pytest -q tests/hito2`.

No hace falta lanzarlos a mano: GitHub los lee en cuanto entran en el
repositorio. Los dos se disparan en los mismos casos, y solo en las
ramas `main` y `master`:

- un **push** (incluido el que acabáis de hacer);
- un **pull request** hacia esas ramas.

Cada push abre **dos máquinas** Ubuntu, independientes. Si el Hito 1
falla, el Hito 2 se ejecuta igual. En cada máquina los pasos son:

1. **Checkout.** Clona el commit que ha disparado el workflow.
2. **Python 3.12.** Instala ese intérprete y guarda la caché de pip
   para no reinstalar desde cero en cada ejecución.
3. **Dependencias.** `pip install -r requirements.txt -r requirements-dev.txt`
   (`requests`, `pandas`, `PyYAML` y `pytest`).
4. **El pytest de ese hito.** El del Hito 1 no lanza el del Hito 2, ni al revés.

El resultado queda en la pestaña **Actions** de este repositorio:
https://github.com/cesar-andress/bigdata2026/actions
Cada ejecución enseña el workflow, el commit, la hora y el registro de
`pytest`. Una cruz roja significa que algún test de ese hito ha fallado.
En este repo docente la cruz es esperable: el starter no cumple el
contrato. Verde solo cuando el `pytest` de ese workflow termina sin fallos.

Esos workflows comprueban **el código de este repositorio**, no el vuestro.
Copiar los dos YAML, `tests/`, `pytest.ini` y `requirements-dev.txt` a
vuestro repo hace que las mismas máquinas se disparen en cada push
vuestro. Mientras no lo copiéis, la forma de ver vuestro estado es la de
la sección anterior (`--repo=`) o la tabla de más arriba, que actualiza
el profesor.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `src/` | Extract / transform / load / fichas |
| `sources.yaml` | Fuentes y países foco |
| `data/` | `raw` → `clean` → `serving` (artefactos locales, no versionados) |
| `tests/hito1/` | Comprobaciones del Hito 1, más la ejecución del ETL actual |
| `tests/hito2/` | Comprobaciones del Hito 2 (Spark y cierre) |
| `.github/workflows/hito1-tests.yml` | CI del Hito 1 |
| `.github/workflows/hito2-tests.yml` | CI del Hito 2 |

## Reglas del framework (no romper)

- **Extract** no limpia ni une fuentes.
- **Transform** no descarga; solo lee `data/raw/`.
- **Load / fichas** no leen JSON bruto; solo `clean/` → `serving/`.
