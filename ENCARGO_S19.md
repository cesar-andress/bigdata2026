# Encargo · Sesión 19 (Tema VII)

Entregar en **vuestro** repositorio de equipo (no en este).

## 1. Kit docente

Dejad constancia del commit de
[`cesar-andress/bigdata2026`](https://github.com/cesar-andress/bigdata2026)
que habéis usado (`git pull` / clon).

## 2. Pytest desde el clon docente

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q tests/hito1 --repo=/ruta/a/vuestro/clon
pytest -q tests/hito2 --repo=/ruta/a/vuestro/clon
```

Pegad o enlazad la salida. Un fallo = el hito no está cumplido.
Prioridad: cerrar Hito 1; después el cierre del Hito 2
(`spark/job_01.py`, `ENTREGA_02.md`, `BUGS.md`, `evidencias/`, tag
`entrega-02`).

## 3. Acta `ACTA_S19.md` (una pantalla)

Cuatro bloques, en prosa breve:

1. **Batch.** Qué hace vuestro `spark/job_01.py` y que el proceso termina.
2. **Streaming.** Qué haría un query `temp-stream` y que permanece hasta
   `stop`.
3. **Tres memorias.** Progreso, estado, checkpoint (una línea cada una).
4. **Ensayo.** Qué demuestra stop/start con la misma
   `checkpointLocation` (`~/checkpoints/temp-stream`). Qué **no**
   demuestra ver filas en consola.

Si ensayáis en DataLab (`admin@datalab`, Kafka `127.0.0.1:9092`, topic
`sensores.temp`), indicad si hubo reanudación. No inventéis cifras ni
capturas.

## Criterio de revisión

No basta la consola. Hace falta pytest + acta de las tres memorias.
