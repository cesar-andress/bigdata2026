# Sesión 20: 23 de noviembre de 2026

Lo que hay que entregar: [`ENCARGO_S20.md`](ENCARGO_S20.md).

## La idea de hoy

En la sesión 19 montasteis (o debíais montar) un programa Spark que
**no termina**. Hoy la pregunta cambia: ¿**debemos** tenerlo siempre
encendido?

Caso A: informe de ocupación a las 08:00 → suele bastar un **batch**
nocturno. Caso B: alerta de aforo en minutos → sí hace falta
**streaming** mientras el edificio está abierto.

Misma materia prima (eventos de aulas). Dos ritmos de consumidor.
Dos arquitecturas.

## Lo que hacéis hoy

**A.** `git pull` de este repo y leed `decision/casos.yaml`.

**B.** Escribid `DECISION_S20.md` (plantilla en
`decision/plantilla_criterio.md`).

**C.** `pytest -q tests/s20 --repo=...`

## Si aún no cerrasteis la sesión 19

[`ENCARGO_S19.md`](ENCARGO_S19.md) sigue pendiente. Hoy se revisa en
aula; no sustituye al criterio de decisión de esta sesión.
