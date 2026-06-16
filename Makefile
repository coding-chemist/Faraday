.PHONY: install dev api worker flower web up down test test-llm lint format clean seed seed-clear embed seed-and-embed parse docker-hf-build docker-hf-run web-build web-preview smoke-llm

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

seed:
	uv run python scripts/seed.py

seed-clear:
	uv run python scripts/seed.py --clear

embed:
	uv run python scripts/embed.py

seed-and-embed: seed-clear embed

test:
	uv run pytest

test-llm:
	uv run pytest -m llm -v

parse:
	@if [ -z "$(Q)" ]; then echo "Usage: make parse Q='your query'"; exit 1; fi
	uv run python scripts/parse_query.py "$(Q)"

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

# --- HF Spaces image ---

docker-hf-build:
	docker build -f infra/hf-spaces/Dockerfile -t faraday-hf .

docker-hf-run:
	@if [ -z "$$FARADAY_LLM_CONFIG__API_KEY" ]; then \
	  echo "WARN: FARADAY_LLM_CONFIG__API_KEY not set — Ollama Cloud calls will fail."; \
	fi
	docker run --rm -p 7860:7860 \
	  -e FARADAY_LLM_CONFIG__API_KEY="$$FARADAY_LLM_CONFIG__API_KEY" \
	  -e FARADAY_CORS_ORIGINS="$${FARADAY_CORS_ORIGINS:-http://localhost:5173}" \
	  faraday-hf

# --- Vercel production bundle smoke test ---

web-build:
	cd apps/web && npm run build

web-preview: web-build
	cd apps/web && npm run preview

# --- LLM secret smoke test ---

smoke-llm:
	@if [ -z "$$FARADAY_API_URL" ]; then \
	  echo "Usage: make smoke-llm FARADAY_API_URL=https://<your-space>.hf.space"; \
	  exit 1; \
	fi
	@echo "Probing $$FARADAY_API_URL/health/llm ..."
	@curl -sS "$$FARADAY_API_URL/health/llm" | python -m json.tool
