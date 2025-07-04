.PHONY: setup run check lint type-check

setup:
	uv venv
	uv pip install -e .[dev]

run:
	uv run python url_monitor.py

check:
	$(MAKE) lint
	$(MAKE) type-check

lint:
	uv run ruff check .

type-check:
	uv run mypy .
