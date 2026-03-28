PY=python

.PHONY: install install-dev test test-cov lint type format run api clean

install:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e .

install-dev: install
	$(PY) -m pip install -r requirements-dev.txt

test:
	$(PY) -m pytest -q

test-cov:
	$(PY) -m pytest -q --cov=stats_engine --cov=literature --cov-report=term-missing

lint:
	$(PY) -m ruff check .

type:
	$(PY) -m mypy .

format:
	$(PY) -m black .

run:
	streamlit run app_streamlit/app.py

api:
	uvicorn api_fastapi.main:app --reload --port 8000

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache __pycache__