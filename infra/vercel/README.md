# Vercel deployment for `apps/web`

The Vite + React frontend deploys to Vercel as a static SPA. The backend
lives on HF Spaces (see `infra/hf-spaces/README.md`); the frontend talks
to it via `VITE_API_BASE_URL`.

## One-time setup

1. **Sign in to Vercel** with your GitHub account.
2. **New Project → Import the repo.**
3. **Root Directory**: `apps/web`. This is the critical setting for
   monorepo projects — without it Vercel tries to build the whole repo.
4. **Framework Preset**: Vite (auto-detected from `apps/web/vercel.json`).
5. Leave Build / Output / Install commands as-is (they're driven by
   `apps/web/vercel.json`).
6. **Deploy.** First build takes ~30s.

## Environment variables

In **Vercel Dashboard → Settings → Environment Variables**:

| Variable | Environment | Value |
|---|---|---|
| `VITE_API_BASE_URL` | Production | `https://<your-username>-faraday.hf.space` |
| `VITE_API_BASE_URL` | Preview | same as Production (or a separate Space for preview backend) |
| `VITE_API_BASE_URL` | Development | leave unset — local dev uses the Vite `/api` proxy |

After changing env vars, **redeploy** (Settings → Deployments → most
recent → ⋯ → Redeploy). Vercel does not auto-rebuild on env var changes.

## Custom domain (optional)

- Vercel → Settings → Domains → Add `faraday.app` (or whatever)
- Update your DNS records as Vercel instructs (CNAME or A records)
- Cert is automatic

## What `vercel.json` controls

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }],
  "headers": [ /* aggressive cache for /assets, daily for /illustrations,
                  no-cache for index.html */ ]
}
```

- **SPA rewrites**: every path serves `/index.html` so client-side routes
  (`/memory/ask`, `/charts-demo`, etc.) work on direct visit / refresh /
  share. Without this, hitting `https://faraday.vercel.app/memory/ask`
  cold would 404 because Vercel would look for a real file.
- **Cache headers**:
  - `/assets/*` → 1 year immutable (hashed filenames, safe)
  - `/illustrations/*` → 1 day (PNG illustrations, may be swapped)
  - `/index.html` → must-revalidate (so deploys land fast)

## CORS — important

The HF Space backend has `FARADAY_CORS_ORIGINS` allowlist + a regex
allowing `*.vercel.app`. Preview URLs (PR deploys) work without further
config because every Vercel domain matches the regex.

If you use a custom domain, add it to the HF Space's
`FARADAY_CORS_ORIGINS` env var. Example:
`https://faraday.app,https://www.faraday.app,https://faraday.vercel.app`

## Smoke test after deploy

1. Visit your Vercel URL (e.g. `https://faraday.vercel.app`)
2. Landing page loads — "Your lab's memory." headline, forest CTA button
3. Click "Open Lab Memory" → navigates to `/memory/ask`
4. Sidebar + watercolor right rail + Watch teaser render
5. Type a query → submit
6. Browser DevTools Network tab: POST `/memory/ask` should go to your
   HF Space URL (not 404 from Vercel)
7. Response should be a JSON `AnalysisResult`; the chart + summary cards
   render

If step 6 fails with 404: `VITE_API_BASE_URL` isn't set in the Production
environment, or the build wasn't redeployed after setting it.

If step 6 fails with CORS error: HF Space's `FARADAY_CORS_ORIGINS` doesn't
include your Vercel URL, or the Space is sleeping (cold start) — the
frontend warm-up ping should have woken it.

## Local production build smoke

Before deploying, you can verify the production bundle locally:

```bash
cd apps/web
VITE_API_BASE_URL=https://<your-space>.hf.space npm run build
npm run preview
```

`vite preview` serves the built `dist/` on `:4173`. Hit `/memory/ask`
and verify the API call works against the real HF Space.

## Image size + perf

Build output is ~700 KB gzipped (MUI is the bulk). Lighthouse score
should be 90+ on a fresh Vercel deploy with Network: Cable.

For deeper perf later:
- `npm run build` + analyze with `vite-bundle-visualizer`
- Code-split MUI icons (only Lab Memory needs Brain; only Ask needs Search)
- Lazy-load ChartsDemo (`React.lazy` on the route)

None of these are needed for v0.1 — the bundle is small enough.
