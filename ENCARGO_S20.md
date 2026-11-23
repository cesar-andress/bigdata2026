# Encargo de la sesión 20 (23/11/2026)

Hoy no montáis un pipeline nuevo. Hoy **decidís** si hace falta.

Se entrega en **vuestro** repositorio: fichero `DECISION_S20.md` en la raíz.

## A. Bajad lo nuevo

```bash
cd bigdata2026 && git pull --ff-only
```

Mirad `decision/casos.yaml` (hechos) y
`decision/plantilla_criterio.md` (forma del documento).

## B. Escribid `DECISION_S20.md`

Dos casos del mismo dominio (ocupación de aulas):

| Caso | Qué es | Conclusión que debe sostenerse con hechos |
| --- | --- | --- |
| A · Informe de las ocho | Consulta diaria 08:00, frescura de horas | **batch** (no streaming 24/7 obligatorio) |
| B · Alerta de aforo | Reacción en menos de 2 minutos | **streaming** (mientras haya riesgo que mitigar) |

En cada caso, rellenad al menos:

- `latencia_util`
- `frescura_admitida`
- `decision`
- `consumidor_continuo`
- `conclusion_arquitectura` (`batch` o `streaming`)
- `por_que_no_la_otra` (una frase)

Más las tres frases del consumidor (quién/cuándo; daño si tarde; valor
si antes).

## C. Pasad el test

Desde el clon de este repo:

```bash
pytest -q tests/s20 --repo=/ruta/a/vuestro/clon
```

Un fallo = el documento no cumple el contrato de hoy.

## Puente con lo anterior

- Sesión 19: sabéis montar un query continuo con checkpoint.
- Hoy: sabéis decir **cuándo no hace falta** montarlo (informe) y
  **cuándo sí** (alerta).
- Quien tenga S19 pendiente: sigue contando
  [`ENCARGO_S19.md`](ENCARGO_S19.md).
