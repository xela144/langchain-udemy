VENV := .venv/
PYTHON := $(VENV)bin/python
UV_PIP := uv pip


develop: venv reinstall
	$(UV_PIP) install -e ".[dev]"

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

.PHONY: streamlit
streamlit:
	$(VENV)/bin/streamlit run src/documentation_helper/main.py
