# Secrets reference

Canonical list of every secret + env var Faraday needs across all three
deployment surfaces: **HF Spaces** (backend), **Vercel** (frontend), and
**local dev**. Pairs with `infra/hf-spaces/README.md` and `infra/vercel/README.md`.

## Quick map

| Secret | Surface | Required? | What it does |
|---|---|---|---|
| `FARADAY_LLM_CONFIG__API_KEY` | HF Space | yes (prod) | Authenticates to Ollama Cloud |
| `FARADAY_CORS_ORIGINS` | HF Space | yes (prod) | Allowlists the Vercel domain(s) for cross-origin API calls |
| `VITE_API_BASE_URL` | Vercel | yes (prod) | Tells the frontend where the API lives |
| `FARADAY_LLM_CONFIG__HOST` | HF Space | no (defaults to `https://ollama.com`) | Swap to local Ollama for dev |
| `FARADAY_LLM_CONFIG__MODEL` | HF Space | no (defaults to `gpt-oss-120b`) | Override the chat model |
| `FARADAY_LLM_CONFIG__EMBED_MODEL` | HF Space | no (defaults to `nomic-embed-text`) | Override the embedding model |

## 1. Ollama Cloud — get the API key

1. Sign in to [ollama.com](https://ollama.com)
2. **Settings → API Keys → Create new key**
3. Copy the key (looks like `ollama_xxxxxxxxxxxxxxxxxxxxxxxx`). You won't
   see it again — save it now.
4. Free tier covers the portfolio demo; rate limits documented on the
   pricing page

## 2. HF Space — set the backend secrets

In your HF Space:
1. **Settings → Variables and secrets**
2. **Add new secret** (NOT variable — secrets are encrypted at rest and
   never logged):

| Name | Value |
|---|---|
| `FARADAY_LLM_CONFIG__API_KEY` | the Ollama Cloud key from step 1 |
| `FARADAY_CORS_ORIGINS` | `https://faraday.vercel.app,https://*.vercel.app` (comma-separated) |

Optional variables (not secrets — these are non-sensitive overrides):

| Name | When to set |
|---|---|
| `FARADAY_LLM_CONFIG__HOST` | If using a non-cloud endpoint |
| `FARADAY_LLM_CONFIG__MODEL` | If you want a different chat model |
| `FARADAY_LLM_CONFIG__EMBED_MODEL` | If you want a different embed model |
| `FARADAY_LOG_LEVEL` | Default INFO; set DEBUG to troubleshoot |

3. **Restart the Space** (Settings → Restart). Env var changes don't
   take effect on running containers.

## 3. Vercel — set the frontend env var

In Vercel dashboard:
1. **Settings → Environment Variables**
2. Add for the **Production** environment:

| Name | Value |
|---|---|
| `VITE_API_BASE_URL` | `https://<your-username>-faraday.hf.space` |

3. Optionally add for **Preview** (same value, or a separate Space if you
   want preview deploys to use a non-prod backend)
4. **Redeploy** the latest deployment so the env var takes effect. Vercel
   does NOT auto-rebuild on env-var changes.

## 4. Local dev — `.env` file

Copy `.env.example` to `.env` at the repo root. The defaults work for
local Ollama (no key needed):

```bash
FARADAY_LLM_PROVIDER=ollama
FARADAY_LLM_CONFIG__HOST=http://localhost:11434
FARADAY_LLM_CONFIG__MODEL=qwen2.5:7b
FARADAY_LLM_CONFIG__EMBED_MODEL=nomic-embed-text
```

If you want to test the Ollama Cloud path locally instead:

```bash
FARADAY_LLM_CONFIG__HOST=https://ollama.com
FARADAY_LLM_CONFIG__API_KEY=ollama_xxxxxxxx
FARADAY_LLM_CONFIG__MODEL=gpt-oss-120b
```

`.env` is gitignored — never commit secrets.

## 5. Smoke test after deploying

After every secret change, hit `/health/llm` to verify the chain works:

```bash
curl https://<your-username>-faraday.hf.space/health/llm
```

Expected response when healthy:

```json
{
  "status": "ok",
  "provider": "ollama",
  "host": "https://ollama.com",
  "cloud": true,
  "embedding_dim": 768,
  "model": "nomic-embed-text"
}
```

Common failure modes:

| Response | Likely cause |
|---|---|
| `503` with `AuthenticationError` | `FARADAY_LLM_CONFIG__API_KEY` is missing or invalid |
| `503` with `ConnectionError` | `FARADAY_LLM_CONFIG__HOST` unreachable (typo, wrong URL) |
| `503` with `NotFoundError` (model) | `FARADAY_LLM_CONFIG__EMBED_MODEL` doesn't exist on the provider |
| `503` with `RateLimitError` | Free tier exhausted — wait or upgrade |
| `cloud: false` in response | `__API_KEY` not picked up — restart the Space after setting |

## 6. Startup warnings

The API logs explicit warnings on boot when production secrets are missing.
Tail the HF Space logs after deploy and look for `startup.secret.missing`:

```
{"event":"startup.secret.missing","level":"warning","detail":"FARADAY_LLM_CONFIG__API_KEY is empty but FARADAY_LLM_CONFIG__HOST targets Ollama Cloud..."}
```

If you see this, the smoke test in step 5 will also fail with 401.

## 7. Rotating secrets

When you need to rotate the Ollama Cloud key:
1. Generate a new key at ollama.com
2. Update `FARADAY_LLM_CONFIG__API_KEY` in HF Space → Settings → Variables and secrets
3. Restart the Space
4. Confirm with `/health/llm`
5. Delete the old key at ollama.com

No code change required — the OllamaProvider reads the key from env at
startup, and the registry pattern means swapping providers entirely is
also one env var (`FARADAY_LLM_PROVIDER=...`).
