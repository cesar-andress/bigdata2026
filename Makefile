# Ayudas locales del repo docente (no es la solución de la práctica).
.PHONY: help deps test-hito1 test-hito2 kit-hoy

help:
	@echo "Objetivos útiles:"
	@echo "  make deps                 # pip install requirements + requirements-dev"
	@echo "  make test-hito1 REPO=...  # pytest tests/hito1 --repo=\$$REPO"
	@echo "  make test-hito2 REPO=...  # pytest tests/hito2 --repo=\$$REPO"
	@echo "  make kit-hoy              # zip con lo nuevo de la sesión 19"

deps:
	pip install -r requirements.txt -r requirements-dev.txt

test-hito1:
	@test -n "$(REPO)" || (echo "Usad: make test-hito1 REPO=/ruta/a/vuestro/clon" >&2; exit 1)
	pytest -q tests/hito1 --repo="$(REPO)"

test-hito2:
	@test -n "$(REPO)" || (echo "Usad: make test-hito2 REPO=/ruta/a/vuestro/clon" >&2; exit 1)
	pytest -q tests/hito2 --repo="$(REPO)"

# Empaqueta lo que los equipos suelen necesitar hoy (tests, CI, checklist).
kit-hoy:
	@rm -f kit_sesion_19.zip
	zip -r kit_sesion_19.zip \
		SESION_19.md ENCARGO_S19.md README.md Makefile \
		requirements.txt requirements-dev.txt pytest.ini conftest.py \
		tests \
		.github/workflows/hito1-tests.yml \
		.github/workflows/hito2-tests.yml \
		-x '*.pyc' -x '*__pycache__*' -x '*.pytest_cache*'
	@echo "Generado: kit_sesion_19.zip"
