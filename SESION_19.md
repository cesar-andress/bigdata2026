# Sesión 19 · 18 de noviembre de 2026 · Tema VII

Checklist de aula para **Spark Structured Streaming** (estado,
checkpointing y recuperación). El material de diapositivas de aula es
`sesiones/sesion_19_tema_07.pdf` en el monorepo del curso; el capítulo
desarrolla la prosa. Este fichero solo orienta qué descargar y qué
demostrar hoy. No inventa capturas ni cifras de laboratorio.

## Entorno de aula (ficha)

| Pieza | Valor |
| --- | --- |
| Host | DataLab · prompt `admin@datalab` |
| Broker Kafka | `127.0.0.1:9092` |
| Topic | `sensores.temp` |
| Checkpoint | `~/checkpoints/temp-stream` (= `/home/admin/checkpoints/temp-stream`) |
| Spark UI (mientras viva la sesión) | `127.0.0.1:4040` |

## Lo nuevo que tenéis que bajar hoy

Fuente: este repositorio docente
[`cesar-andress/bigdata2026`](https://github.com/cesar-andress/bigdata2026).

```bash
git clone git@github.com:cesar-andress/bigdata2026.git
# o, si ya lo teníais:
cd bigdata2026 && git pull --ff-only
```

Hoy lo útil es, sobre todo:

1. `SESION_19.md` (este checklist).
2. `tests/hito1/`, `tests/hito2/`, `tests/conftest.py` (opción `--repo`).
3. `requirements.txt` (incluye `pyarrow`) y `requirements-dev.txt`.
4. `.github/workflows/hito1-tests.yml` y `hito2-tests.yml` (si queréis
   CI en vuestro repo: copiad esos YAML + `tests/` + `pytest.ini` +
   `requirements-dev.txt`).
5. La sección «Estado de los equipos» del `README.md` (quién pasa y
   qué arreglar).

No trabajéis encima de este clon: el código de entrega sigue en
**vuestro** repositorio de equipo.

## Comprobar vuestro código (Hito 1 / Hito 2)

Desde este clon docente, sin copiar `tests/` al vuestro:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q tests/hito1 --repo=/ruta/a/vuestro/clon
pytest -q tests/hito2 --repo=/ruta/a/vuestro/clon
```

Un solo fallo = el hito no está cumplido. Si pytest dice
`unrecognized arguments: --repo`, el `tests/conftest.py` está
desfasado: volved a sacar este repo.

## Qué se pide demostrar en aula hoy

1. **Batch ↔ streaming.** El `spark/job_01.py` de la Entrega 2 es
   *batch*: lee, calcula, escribe y termina. El query de hoy
   (`temp-stream`) permanece activo (micro-lotes). Misma familia Spark;
   ciclo de vida distinto.
2. **Continuidad tras `stop`/`start`.** Misma definición y la **misma**
   `checkpointLocation` (`~/checkpoints/temp-stream`). Ver filas en
   consola **no** basta: hay que reanudar progreso (y estado de ventanas
   si el plan agrega).
3. **Tres memorias, con nombre:**
   - **progreso** — hasta dónde se leyó la fuente;
   - **estado** — agregados / ventanas abiertos (aquí sí, por ventana);
   - **checkpoint** — dónde sobreviven las dos anteriores.
4. **No confundir** `startingOffsets=earliest` / `latest` *sin*
   checkpoint con «recuperación». Sin ruta estable, cada arranque es
   un primer día.

## Puente con la Entrega 2

Quien aún no cierra Hito 1 / Hito 2: el puente de aula es el contraste
batch ↔ streaming con vuestro (o el del starter) `spark/job_01.py`.
El checklist mínimo de cierre y el estado por equipo están en el
`README.md` de este repositorio.
