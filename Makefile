.PHONY: install dev api worker flower web up down test lint format clean

install:
	uv sync

dev: up
	@echo "Stack up. Run 'make api', 'make worker', 'make web' in separate terminals."

api:
	uv run uvicorn faraday_api.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	uv run celery -A faraday_worker.celery_app worker -l info

flower:
	uv run celery -A faraday_worker.celery_app flower --port=5555

web:
	cd apps/web && npm run dev

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run mypy engine/src shared/src apps/api/src apps/worker/src

format:
	uv run ruff format .
	uv run ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
