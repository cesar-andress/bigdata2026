"""Sesión 19: query continuo ``temp-stream`` (Spark Structured Streaming).

Starter para copiar a **vuestro** repositorio como ``streaming/temp_stream.py``.
Hay seis huecos marcados ``TODO`` (T1 a T6). Cuando estén resueltos no debe
quedar ningún ``TODO`` ni ningún ``NotImplementedError`` en el fichero.

Contrato de aula (DataLab, ``admin@datalab``):

* broker Kafka ``127.0.0.1:9092``, topic ``sensores.temp``;
* eventos JSON ``{"sensor": "s01", "valor": 22.5, "ts": "2026-11-18T12:00:00Z"}``;
* conteo por ventana de 1 minuto y por sensor, watermark de 10 minutos;
* sink ``console`` en modo ``update``, trigger de 5 segundos;
* ``checkpointLocation`` estable: ``~/checkpoints/temp-stream``.

Reto sorpresa (T6): un segundo query, ``temp-nulos``, que muestra los
eventos cuyo ``valor`` llega nulo (esquema roto). Tiene **su propio**
checkpoint, ``~/checkpoints/temp-nulos``: dos queries nunca comparten ruta.

Arranque (el conector Kafka va aparte de PySpark):

    spark-submit \\
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.9 \\
      streaming/temp_stream.py

Ctrl+C detiene el query (equivale a ``q.stop()``). Volver a lanzar el mismo
comando con la misma ruta de checkpoint es la prueba de parar y arrancar.
"""

from __future__ import annotations

import argparse
import os

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json, window
from pyspark.sql.types import DoubleType, StringType, StructType, TimestampType

BROKER = "127.0.0.1:9092"
TOPIC = "sensores.temp"
CHECKPOINT = os.path.expanduser("~/checkpoints/temp-stream")
QUERY_NAME = "temp-stream"
CHECKPOINT_NULOS = os.path.expanduser("~/checkpoints/temp-nulos")
QUERY_NULOS = "temp-nulos"


def construir_fuente(spark: SparkSession, starting_offsets: str) -> DataFrame:
    """T1. Fuente Kafka.

    ``readStream`` con ``format("kafka")``, el broker ``BROKER``, suscrito a
    ``TOPIC`` y ``startingOffsets`` = ``starting_offsets``. Recordad:
    ``startingOffsets`` solo cuenta si el checkpoint aún no tiene progreso.
    """
    # TODO T1: devolver el DataFrame de streaming leído de Kafka.
    raise NotImplementedError("T1: fuente Kafka")


def parsear(df: DataFrame) -> DataFrame:
    """T2. de ``value`` (bytes) a JSON y a columnas tipadas ``sensor``, ``valor``, ``ts``."""
    esquema = (
        StructType()
        .add("sensor", StringType())
        .add("valor", DoubleType())
        .add("ts", TimestampType())
    )
    # TODO T2: CAST(value AS STRING), from_json(..., esquema) y quedarse con d.*
    raise NotImplementedError("T2: parseo JSON")


def agregar(ev: DataFrame) -> DataFrame:
    """T3. Estado: watermark de 10 minutos sobre ``ts`` y conteo por
    ``window(ts, "1 minute")`` y ``sensor``."""
    # TODO T3: withWatermark + groupBy(window, sensor) + count
    raise NotImplementedError("T3: ventana y watermark")


def arrancar(agg: DataFrame, checkpoint: str):
    """T4. Sink: console, ``outputMode("update")``, ``checkpointLocation``
    = ``checkpoint``, ``trigger(processingTime="5 seconds")``,
    ``queryName(QUERY_NAME)`` y ``start()``. Devuelve el query."""
    # TODO T4: writeStream ... start()
    raise NotImplementedError("T4: writeStream con checkpoint")


def vigilar_nulos(ev: DataFrame, checkpoint: str):
    """T6. Reto sorpresa. Segundo query sobre los mismos eventos parseados:
    ``filter(col("valor").isNull())``, sink console en modo ``append``,
    ``checkpointLocation`` = ``checkpoint`` (¡distinta de la de temp-stream!),
    ``queryName(QUERY_NULOS)``, mismo trigger y ``start()``."""
    # TODO T6: writeStream de los eventos con valor nulo
    raise NotImplementedError("T6: query temp-nulos")


def main() -> None:
    p = argparse.ArgumentParser(description="Query continuo temp-stream (S19)")
    p.add_argument("--checkpoint", default=CHECKPOINT)
    p.add_argument(
        "--starting-offsets",
        default="earliest",
        choices=["earliest", "latest"],
        help="Frontera inicial; ignorada si el checkpoint ya tiene progreso.",
    )
    p.add_argument("--checkpoint-nulos", default=CHECKPOINT_NULOS)
    args = p.parse_args()

    spark = SparkSession.builder.appName(QUERY_NAME).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    ev = parsear(construir_fuente(spark, args.starting_offsets))
    q = arrancar(agregar(ev), args.checkpoint)
    qn = vigilar_nulos(ev, args.checkpoint_nulos)
    for query, ruta in ((q, args.checkpoint), (qn, args.checkpoint_nulos)):
        print(f"query={query.name} id={query.id} checkpoint={ruta}")

    # TODO T5: esperar (spark.streams.awaitAnyTermination()) y, si se
    # interrumpe con Ctrl+C, parar los dos queries con stop() sin borrar
    # ningún checkpoint.
    raise NotImplementedError("T5: esperar y parar limpio")


if __name__ == "__main__":
    main()
