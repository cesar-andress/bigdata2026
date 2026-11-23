"""S20: DECISION_S20.md — criterio batch frente a streaming.

Comprobación estática del documento de decisión. No arranca Spark ni
Kafka. Que pase no demuestra que el diseño esté desplegado: demuestra
que el criterio está escrito con los campos mínimos y conclusiones
coherentes con los dos casos de aula.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.s20

NOMBRE = "DECISION_S20.md"

FALTA = (
    "Falta DECISION_S20.md en la raíz de vuestro repo. Copiad la plantilla "
    "de cesar-andress/bigdata2026 (decision/plantilla_criterio.md), "
    "rellenadla y renombradla a DECISION_S20.md."
)

CAMPOS = (
    "latencia_util",
    "frescura_admitida",
    "decision",
    "consumidor_continuo",
    "conclusion_arquitectura",
    "por_que_no_la_otra",
)


def _buscar(repo_root: Path, git_root: Path) -> Path | None:
    for base in (repo_root, git_root):
        if (base / NOMBRE).is_file():
            return base / NOMBRE
    return None


def test_existe_decision_s20(repo_root: Path, git_root: Path):
    if _buscar(repo_root, git_root) is None:
        pytest.fail(FALTA)


@pytest.fixture(scope="module")
def texto(repo_root: Path, git_root: Path) -> str:
    path = _buscar(repo_root, git_root)
    if path is None:
        pytest.skip("sin DECISION_S20.md (ver test_existe_decision_s20)")
    return path.read_text(encoding="utf-8")


def test_nombra_los_dos_casos(texto: str):
    bajo = texto.lower()
    assert "informe" in bajo or "ocho" in bajo or "08:00" in bajo, (
        "El documento debe tratar el caso del informe diario (consulta 08:00)."
    )
    assert "alerta" in bajo or "aforo" in bajo, (
        "El documento debe tratar el caso de la alerta de aforo."
    )


def test_campos_minimos(texto: str):
    bajo = texto.lower()
    faltan = [c for c in CAMPOS if c not in bajo]
    assert not faltan, (
        "Faltan campos del criterio: " + ", ".join(faltan) + ". "
        "Usad la plantilla de decision/plantilla_criterio.md."
    )


def test_informe_concluye_batch(texto: str):
    """Cerca del bloque del informe debe aparecer conclusion batch."""
    bajo = texto.lower()
    # Trozo aproximado: desde "informe"/"ocho" hasta "alerta"/"aforo"
    m = re.search(
        r"(informe|ocho|08:00).{0,1200}?(alerta|aforo)",
        bajo,
        flags=re.DOTALL,
    )
    bloque = m.group(0) if m else bajo[:1500]
    assert re.search(r"conclusion_arquitectura\s*:\s*batch\b", bloque), (
        "En el caso del informe, conclusion_arquitectura debe ser batch "
        "(no streaming 24/7 obligatorio)."
    )


def test_alerta_concluye_streaming(texto: str):
    bajo = texto.lower()
    m = re.search(r"(alerta|aforo).{0,1200}", bajo, flags=re.DOTALL)
    bloque = m.group(0) if m else bajo[-1500:]
    assert re.search(r"conclusion_arquitectura\s*:\s*streaming\b", bloque), (
        "En el caso de la alerta de aforo, conclusion_arquitectura debe ser streaming."
    )


def test_no_solo_esloganes(texto: str):
    """Debe haber algo más que moda: números o hechos del caso."""
    bajo = texto.lower()
    hechos = [
        "08:00",
        "8:00",
        "02:00",
        "2 min",
        "2 minutos",
        "< 2",
        "180",
        "noche",
        "horas",
        "minutos",
    ]
    assert any(h in bajo for h in hechos), (
        "El criterio debe anclarse a hechos del caso (hora de consulta, "
        "frescura, umbral de minutos, volumen, etc.), no solo a adjetivos."
    )


def test_menciona_las_tres_frases_o_equivalente(texto: str):
    bajo = texto.lower()
    pistas = ("consumidor", "tarde", "antes", "quién", "quien", "daño", "acción", "accion")
    assert sum(1 for p in pistas if p in bajo) >= 2, (
        "Incluid las tres frases del consumidor (quién/cuándo; daño si tarde; "
        "valor si antes) o equivalentes claros."
    )
