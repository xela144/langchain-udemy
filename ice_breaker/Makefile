VENV := .venv/
PYTHON := $(VENV)bin/python
UV_PIP := uv pip
-include .env
DATA_SRV ?= data/


reinstall:
	$(UV_PIP) install -e .

develop: venv reinstall
	$(UV_PIP) install -e ".[dev]"

flask:
	FLASK_APP=ice_breaker.app $(VENV)bin/flask run

local-server:
	$(PYTHON) -m http.server -d $(DATA_SRV)

.PHONY: venv
venv:
	uv venv --python=3.12

.PHONY: format
format:
	$(PYTHON) -m black .
	$(PYTHON) -m ruff format .

.PHONY: lint
lint:
	$(PYTHON) -m ruff check .

.PHONY: lint-fix
lint-fix:
	$(PYTHON) -m ruff check --fix .

.PHONY: check
check: format lint
