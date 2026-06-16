# Faraday HF Spaces image — FastAPI + Celery worker + Redis in one container.
#
# Ollama NOT bundled. The OllamaProvider talks to Ollama Cloud over HTTPS via
# the FARADAY_LLM_CONFIG__HOST + __API_KEY env vars (set as HF Space secrets).
# This keeps the image ~700-900MB, no GPU dependency, and lets the free CPU
# tier handle the demo workload.
#
# Frontend lives on Vercel — NOT in this image. .dockerignore excludes apps/web.

FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    FARADAY_ENV=prod \
    FARADAY_LOG_JSON=true \
    FARADAY_LOG_LEVEL=INFO \
    FARADAY_DATABASE_URL=sqlite:///./data/faraday.db \
    REDIS_URL=redis://127.0.0.1:6379/0 \
    CELERY_BROKER_URL=redis://127.0.0.1:6379/0 \
    CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1 \
    FARADAY_VECTOR__PROVIDER=faiss \
    FARADAY_VECTOR__CONFIG__INDEX_PATH=/app/data/faiss_index \
    FARADAY_LLM__PROVIDER=ollama \
    FARADAY_LLM__CONFIG__HOST=https://ollama.com \
    FARADAY_LLM__CONFIG__MODEL=gpt-oss:20b \
    FARADAY_LLM__CONFIG__EMBED_MODEL=nomic-embed-text

# System packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      redis-server \
      supervisor \
      curl \
    && rm -rf /var/lib/apt/lists/*

# uv — fast Python package manager, copied from official image
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

WORKDIR /app

# Project files (apps/web excluded via .dockerignore)
COPY pyproject.toml ./
COPY shared shared/
COPY engine engine/
COPY apps/api apps/api/
COPY apps/worker apps/worker/
COPY scripts scripts/

# Install workspace + deps (no dev tools)
RUN uv sync --no-dev

# Writable runtime directory for SQLite + FAISS
RUN mkdir -p /app/data && chmod 777 /app/data

# Supervisord process orchestration
COPY supervisord.conf /etc/supervisor/conf.d/faraday.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# HF Spaces default port
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://127.0.0.1:7860/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
