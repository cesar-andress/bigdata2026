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

## Lo nuevo · 18 de noviembre de 2026 (sesión 19)

Hoy en aula es el **Tema VII**: Spark Structured Streaming (estado,
checkpointing y recuperación) en DataLab. Este repo es la fuente de
«lo nuevo» para comprobar entregas y orientar la sesión.

### Qué descargar / actualizar

```bash
git clone https://github.com/cesar-andress/bigdata2026.git
# si ya lo teníais:
cd bigdata2026 && git pull --ff-only
```

También podéis pedir al profesor el `kit_sesion_19.zip` (`make kit-hoy`
en este clon): tests, workflows, `SESION_19.md`, `ENCARGO_S19.md` y
dependencias.

Leed primero **[`SESION_19.md`](SESION_19.md)** (checklist de aula:
batch ↔ streaming, tres memorias, checkpoint
`~/checkpoints/temp-stream`, Kafka `127.0.0.1:9092` / `sensores.temp`).

### Cómo lanzar los tests contra vuestro clon

```bash
pip install -r requirements.txt -r requirements-dev.txt   # pyarrow incluido
pytest -q tests/hito1 --repo=/ruta/a/vuestro/clon
pytest -q tests/hito2 --repo=/ruta/a/vuestro/clon
# o: make test-hito1 REPO=/ruta/a/vuestro/clon
```

La opción es `--repo` (registrada en `tests/conftest.py`). Un solo
fallo = el hito no pasa. Detalle de la sesión y del estado por equipo:
más abajo y en `SESION_19.md`.

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

La opción es `--repo` (no `--test`). Pytest la registra en
`tests/conftest.py`, así que vale `--repo=/ruta` y también
`--repo /ruta`. Si pytest responde `unrecognized arguments: --repo`
o `no option named '--repo'`, estáis con una copia antigua de
`tests/conftest.py`: volved a copiar ese fichero. También vale
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

## Sesión de hoy · 18 de noviembre de 2026 (sesión 19)

Checklist corto y comandos de descarga: **[`SESION_19.md`](SESION_19.md)**.

Hoy en aula es el **Tema VII**: arquitectura del cómputo continuo en
**Spark Structured Streaming** (estado, checkpointing y recuperación),
sobre DataLab (`admin@datalab`), Kafka en `127.0.0.1:9092` y el topic
`sensores.temp`. Checkpoint de aula: `~/checkpoints/temp-stream`.

### Qué se os va a pedir en la sesión

1. **Contraste batch ↔ streaming.** El `spark/job_01.py` de la Entrega 2
   es un job *batch*: lee Parquet, calcula, escribe y termina. El query
   de hoy permanece activo: micro-lotes, progreso y, si hay agregación
   por ventana, estado. Misma familia Spark; ciclo de vida distinto.
2. **Demostrar continuidad, no solo filas.** Tras un `stop` y un nuevo
   arranque con la **misma** `checkpointLocation`
   (`~/checkpoints/temp-stream`), el query debe reanudar progreso (y
   estado de ventanas si aplica). Ver filas en consola **no** basta.
3. **Nombrar las tres memorias:** progreso (hasta dónde se leyó),
   estado (agregados abiertos) y checkpoint (dónde sobreviven).
4. **No confundir** `startingOffsets=earliest` / `latest` sin checkpoint
   con «recuperación». Sin checkpoint estable, cada arranque es un
   primer día.

Quien aún no cierra la Entrega 2: el puente de aula es ese contraste.
El checklist de más abajo indica el arreglo mínimo para que
`pytest tests/hito1` y `tests/hito2` pasen a cero fallos en vuestro clon.

## Estado de los equipos (18 de noviembre de 2026)

Comprobado hoy contra la rama por defecto de cada GitHub, con
`pytest tests/hito1` y `pytest tests/hito2` de este repositorio
(`pyarrow` instalado). **Pasar** = cero fallos.

Límites oficiales: Hito 1 · **4/11/2026**; Hito 2 · **11/11/2026 23:59**
(marca = fecha de la etiqueta anotada `entrega-02` en GitHub).

| Repositorio | Commit / situación | Hito 1 | ¿Pasa? | Hito 2 | ¿Pasa? | `entrega-02` |
| --- | --- | --- | --- | --- | --- | --- |
| [rmmenendez05/dsbd-big-data-repo](https://github.com/rmmenendez05/dsbd-big-data-repo) | `ca0cafd` · 11/11/2026 | 65 passed | **Sí** | 20 passed | **Sí** | sí (11/11 10:16) |
| [nasratullahjabarkhil/bigdata](https://github.com/nasratullahjabarkhil/bigdata) | `3b9282f` · 17/11/2026 | 64 passed, 1 failed | No | 2 passed, 18 failed | No | no |
| [uag8076-web/BigData2026](https://github.com/uag8076-web/BigData2026) | `9bcf8c2` · 04/11/2026 | 53 passed, 3 failed, 9 skipped | No | 1 passed, 19 failed | No | no |
| [marcosgale/BigData_Proyecto](https://github.com/marcosgale/BigData_Proyecto) | `f18abfd` · 04/11/2026 (código bajo `practica_01_BigData_starter/`) | 47 passed, 17 failed, 1 skipped | No | 0 passed, 20 failed | No | no |
| [edurlix/BigDataProject](https://github.com/edurlix/BigDataProject) | `3b2cc43` · 04/11/2026 | 36 passed, 29 failed | No | 1 passed, 19 failed | No | no |
| [hracjc/dsbd_etl_1](https://github.com/hracjc/dsbd_etl_1) | **404** en GitHub (repo ausente) | no medible | No | no medible | No | — |
| [Sumitodemarmeto/Practica_02_BigData](https://github.com/Sumitodemarmeto/Practica_02_BigData) | **404** en GitHub (repo ausente) | no medible | No | no medible | No | — |

Solo un equipo cumple hoy ambos hitos con etiqueta de entrega.
El resto: o bien queda un fallo de contrato, o el cierre del Hito 2
no está, o el repositorio ya no es público / no existe.

## Problemas y arreglos (para pasar los tests)

### [rmmenendez05/dsbd-big-data-repo](https://github.com/rmmenendez05/dsbd-big-data-repo) — cumple

Rodrigo Moreno Menéndez (`rodrigo.morenom@alumno.ucjc.edu`).
`spark/job_01.py`, `ENTREGA_02.md`, `BUGS.md`, `evidencias/`, tag
`entrega-02`, Actions en verde. En aula: usad vuestro job *batch* como
contraste con el query de Structured Streaming de hoy.

### [nasratullahjabarkhil/bigdata](https://github.com/nasratullahjabarkhil/bigdata) — 1 fallo del Hito 1

Nasratullah Jabarkhil. Casi cierra el Hito 1.

| Problema | Arreglo |
| --- | --- |
| Banco Mundial con `country/{iso2}/...` (un GET por país del foco) | URL `country/all/indicator/...`, paginación contra `total`; sin `{iso2}`/`{iso3}` en la plantilla |
| Sin `spark/job_01.py`, `ENTREGA_02.md`, `BUGS.md`, `evidencias/`, tag `entrega-02` | Completar el cierre del Hito 2 del enunciado |

### [uag8076-web/BigData2026](https://github.com/uag8076-web/BigData2026) — 3 fallos del Hito 1

| Problema | Arreglo |
| --- | --- |
| No hay `CONTRIBUTORS.md` | Nombre, apellidos y correo `@…ucjc.edu` en la raíz |
| `excluded_entities.csv` usa `code` | Columna `source_code` (contrato del enunciado) |
| User-Agent `CAMBIAD_ESTO` | Identificar al equipo de verdad |
| Sin cierre Hito 2 | `spark/job_01.py` + piezas B/C + tag `entrega-02` |

### [marcosgale/BigData_Proyecto](https://github.com/marcosgale/BigData_Proyecto) — 17 fallos; árbol anidado

El ETL vive en `practica_01_BigData_starter/`. Marcos + Alejandro Nieto
en el historial; sin `CONTRIBUTORS.md` institucional.

| Problema | Arreglo |
| --- | --- |
| Código no está en la raíz del repo | Subir `src/`, `sources.yaml`, etc. a la raíz (o que `--repo` apunte al subdirectorio y documentarlo; la etiqueta y el clon limpio del enunciado esperan la raíz) |
| Sin `CONTRIBUTORS.md` | Correos `@…ucjc.edu` |
| Sin `--force` / se guardan no-200 en raw / 404 no explícito | Extract: no escribir raw si status ≠ 200; no reintentar 404; `--force` regenera |
| Ficha sin mediana de región / año | `build_cards` con mediana regional del mismo indicador y año |
| Sin Hito 2 | Job Spark + documentación + tag |

### [edurlix/BigDataProject](https://github.com/edurlix/BigDataProject) — sigue cerca del starter

Eddyson Ureña (CONTRIBUTORS ya añadido). Sigue fallando Parquet Hive,
mediana en fichas y casi todo el Hito 2.

| Problema | Arreglo |
| --- | --- |
| Indicators/languages no en Parquet Hive | `data/clean/indicators/indicator_id=<id>/` + `pyarrow` en `requirements.txt` |
| Comparación de ficha no es mediana regional | Misma regla que el enunciado del Hito 1 |
| Sin Spark ni cierre | Como el checklist del Hito 2 más arriba |

### Repos ausentes (404)

[hracjc/dsbd_etl_1](https://github.com/hracjc/dsbd_etl_1) y
[Sumitodemarmeto/Practica_02_BigData](https://github.com/Sumitodemarmeto/Practica_02_BigData)
ya no resolvían en GitHub el 18/11. Sin URL pública no hay medición ni
etiqueta. Hay que **restaurar el repo** (o publicar uno nuevo y avisar
al profesor) antes de cualquier revisión.

### Checklist mínimo del Hito 2 (quien aún no lo tenga)

1. `spark/job_01.py` ejecutable: tres vías (RDD / DataFrame / Spark SQL)
   alineadas con SQLite; Parquet en `data/serving/spark/cobertura_decada/`;
   event log en `logs/spark-events/`.
2. `ENTREGA_02.md` + `BUGS.md` (≥ 3 defectos).
3. Copiar el event log a `evidencias/`.
4. `.gitignore` con `data/`, `logs/`, `.venv/`.
5. `git tag -a entrega-02` y `git push origin entrega-02`.

## Nota histórica (4 de noviembre de 2026)

Ese día **ningún** equipo pasaba ningún hito. El detalle de aquella
pasada quedó en el historial Git de este README (`7c88b52` /
`0aa4166`). La tabla canónica es la del **18 de noviembre** de arriba.

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
   (`requests`, `pandas`, `PyYAML`, `pyarrow` y `pytest`).
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
vuestro. `--repo` se declara dentro de `tests/conftest.py`; no hace
falta el `conftest.py` de la raíz. Mientras no lo copiéis, la forma de
ver vuestro estado es la de la sección anterior (`--repo`) o la tabla
de más arriba, que actualiza el profesor.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `SESION_19.md` | Checklist de aula (18/11 · Structured Streaming) |
| `ENCARGO_S19.md` | Entrega tras la clase (pytest + acta) |
| `Makefile` | `deps`, `test-hito1`/`test-hito2` con `REPO=…`, `kit-hoy` |
| `src/` | Extract / transform / load / fichas |
| `sources.yaml` | Fuentes y países foco |
| `data/` | `raw` → `clean` → `serving` (artefactos locales, no versionados) |
| `tests/hito1/` | Comprobaciones del Hito 1, más la ejecución del ETL actual |
| `tests/hito2/` | Comprobaciones del Hito 2 (Spark y cierre) |
| `tests/conftest.py` | Registra `--repo` / `DSBD_REPO` |
| `.github/workflows/hito1-tests.yml` | CI del Hito 1 |
| `.github/workflows/hito2-tests.yml` | CI del Hito 2 |

## Reglas del framework (no romper)

- **Extract** no limpia ni une fuentes.
- **Transform** no descarga; solo lee `data/raw/`.
- **Load / fichas** no leen JSON bruto; solo `clean/` → `serving/`.
