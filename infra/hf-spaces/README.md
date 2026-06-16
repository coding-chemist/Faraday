---
title: Faraday API
emoji: 🧪
colorFrom: green
colorTo: emerald
sdk: docker
app_port: 7860
pinned: false
short_description: AI-assisted lab notebook backend — Lab Memory Ask mode
---

# Faraday API · HF Space backend

This Space hosts the backend services for [Faraday](https://github.com/coding-chemist/Faraday).
The frontend lives on Vercel — only the API is here.

## What runs inside

One container with three processes under `supervisord`:

| Process | Port | Public? | Purpose |
|---|---|---|---|
| `uvicorn` (FastAPI) | 7860 | yes | `/health`, `/providers`, `/memory/ask` |
| `redis-server` | 6379 | localhost only | Celery broker + result backend |
| `celery worker` | — | no | Embedding tasks, async work |

Ollama is **not bundled**. LLM calls go to Ollama Cloud over HTTPS via the
`FARADAY_LLM_CONFIG__HOST` + `FARADAY_LLM_CONFIG__API_KEY` env vars.

First container start: SQLite tables created + 210 seed experiments inserted
(idempotent — subsequent starts skip the seed if the DB is already populated).

## Deployment

### 1. Create the Space
- New Space → **Docker** SDK
- Hardware: CPU Basic (free tier is fine for the demo)
- Push this repo's contents to the Space's git remote

### 2. Set secrets (Settings → Variables and secrets)

Required:
- `FARADAY_LLM_CONFIG__API_KEY` — your Ollama Cloud API key
- `FARADAY_CORS_ORIGINS` — comma-separated frontend origins, e.g.
  `https://faraday.vercel.app,https://*.vercel.app`

Optional overrides (sensible defaults baked into the Dockerfile):
- `FARADAY_LLM_CONFIG__HOST` — default `https://ollama.com`
- `FARADAY_LLM_CONFIG__MODEL` — default `gpt-oss-120b`
- `FARADAY_LLM_CONFIG__EMBED_MODEL` — default `nomic-embed-text`

### 3. Push
The Space auto-builds on push. First build is ~3-5 min (cold uv resolve);
subsequent builds are fast (Docker layer cache).

### 4. Verify
- `https://<your-space>.hf.space/health` should return `{"status":"ok",…}`
- `https://<your-space>.hf.space/providers` should list registered LLM + vector providers
- `POST https://<your-space>.hf.space/memory/ask` with `{"query": "..."}` should return an AnalysisResult

## Local testing

Build from the repo root:

```bash
docker build -f infra/hf-spaces/Dockerfile -t faraday-hf .
```

Run:

```bash
docker run --rm -p 7860:7860 \
  -e FARADAY_LLM_CONFIG__API_KEY="$OLLAMA_API_KEY" \
  -e FARADAY_CORS_ORIGINS=http://localhost:5173 \
  faraday-hf
```

Then `http://localhost:7860/health` and `http://localhost:7860/providers`.

## Image size

~800 MB. Trimmed by:
- `python:3.11-slim` base (not full python)
- `apps/web/` excluded via `.dockerignore` (frontend is on Vercel)
- No dev dependencies (`uv sync --no-dev`)
- `UV_COMPILE_BYTECODE=1` for slightly smaller wheels
- No Ollama binary (~700 MB saved) and no bundled models (~4 GB saved)

If image size ever becomes a problem, the next step is multi-stage build with
a `--frozen` uv lock file + Alpine base.

## Cold start

HF Spaces free tier sleeps after ~48h inactivity. First request after sleep
takes 20-40s. The Vercel frontend already handles this with a `/health` warm-up
ping on mount + a "warming up the lab…" toast if >3s.
