"""Fixtures locales para las comprobaciones del Hito 1 (Entrega 2)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
import yaml


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "hito1: comprobaciones del Hito 1 (04/11) de la Entrega 2",
    )


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Raíz del proyecto ETL (donde viven sources.yaml y src/)."""
    here = Path(__file__).resolve()
    for candidate in [here.parents[2], *here.parents]:
        if (candidate / "sources.yaml").is_file() and (candidate / "src").is_dir():
            return candidate
    pytest.fail(
        "No se encuentra la raíz del ETL (sources.yaml + src/). "
        "Colocad tests/hito1/ dentro del repositorio de la práctica."
    )


@pytest.fixture(scope="session")
def git_root(repo_root: Path) -> Path:
    """Raíz Git del clon (puede coincidir con repo_root o ser un padre)."""
    for candidate in [repo_root, *repo_root.parents]:
        if (candidate / ".git").exists():
            return candidate
    return repo_root


@pytest.fixture(scope="session")
def sources_yaml(repo_root: Path) -> dict:
    path = repo_root / "sources.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "sources.yaml debe deserializar a un mapeo"
    return data


@pytest.fixture(scope="session")
def extract_path(repo_root: Path) -> Path:
    path = repo_root / "src" / "extract.py"
    if not path.is_file():
        pytest.fail("Falta src/extract.py; sin extract no hay Hito 1.")
    return path


@pytest.fixture(scope="session")
def extract_source(extract_path: Path) -> str:
    return extract_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def extract_tree(extract_source: str) -> ast.AST:
    return ast.parse(extract_source)
