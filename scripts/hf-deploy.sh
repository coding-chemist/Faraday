#!/usr/bin/env bash
# Deploy Faraday backend to a Hugging Face Space.
#
# What it does:
#   1. Clones the (already-created) HF Space repo into a temp dir
#   2. Wipes whatever's there, copies the deployment-ready file layout
#      (Dockerfile + supervisord + entrypoint + Python source at root)
#   3. Commits + pushes — HF builds the Docker image automatically
#
# Prereqs (one-time):
#   - HF account at huggingface.co
#   - Space created at https://huggingface.co/new-space
#     Name: faraday (or whatever; pass space-name as $1)
#     SDK: Docker
#     Hardware: CPU Basic (free is fine for the demo)
#   - HF token at https://huggingface.co/settings/tokens (Write scope)
#   - export HF_TOKEN=hf_xxxxxxx
#
# After running this:
#   - Watch the build at https://huggingface.co/spaces/<space>/logs
#   - Set FARADAY_LLM_CONFIG__API_KEY and FARADAY_CORS_ORIGINS in
#     Space → Settings → Variables and secrets
#   - Restart the Space, then curl <space>.hf.space/health/llm to verify

set -euo pipefail

SPACE="${1:-coding-chemist/faraday}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKDIR="$(mktemp -d)"

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "ERROR: HF_TOKEN not set."
  echo "  Get one at https://huggingface.co/settings/tokens (Write access)"
  echo "  Then: export HF_TOKEN=hf_xxxxxxxxx"
  exit 1
fi

echo "→ Repo root: $REPO_ROOT"
echo "→ HF Space:  $SPACE"
echo "→ Workdir:   $WORKDIR"
echo

# 1. Clone the Space repo with token-authenticated URL
echo "→ Cloning HF Space repo…"
git clone "https://USER:${HF_TOKEN}@huggingface.co/spaces/${SPACE}" "$WORKDIR/space" 2>&1 | sed 's/^/  /'
cd "$WORKDIR/space"

# 2. Wipe existing files (keep .git so commit history is preserved)
echo "→ Clearing previous deploy artifacts…"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# 3. Copy deployment-ready layout
echo "→ Copying files into Space layout…"

# Root-level files HF Spaces expects at the repo root
cp "$REPO_ROOT/infra/hf-spaces/Dockerfile" Dockerfile
cp "$REPO_ROOT/infra/hf-spaces/supervisord.conf" supervisord.conf
cp "$REPO_ROOT/infra/hf-spaces/entrypoint.sh" entrypoint.sh
cp "$REPO_ROOT/infra/hf-spaces/README.md" README.md  # has HF frontmatter
cp "$REPO_ROOT/.dockerignore" .dockerignore
cp "$REPO_ROOT/pyproject.toml" pyproject.toml

# The Dockerfile references "infra/hf-spaces/supervisord.conf" and
# "infra/hf-spaces/entrypoint.sh" — rewrite those to root-level here
sed -i.bak 's|infra/hf-spaces/supervisord.conf|supervisord.conf|g; s|infra/hf-spaces/entrypoint.sh|entrypoint.sh|g' Dockerfile
rm -f Dockerfile.bak
chmod +x entrypoint.sh

# Python workspace packages
cp -r "$REPO_ROOT/shared" shared
cp -r "$REPO_ROOT/engine" engine
mkdir -p apps
cp -r "$REPO_ROOT/apps/api" apps/api
cp -r "$REPO_ROOT/apps/worker" apps/worker
cp -r "$REPO_ROOT/scripts" scripts

# 4. Commit + push
echo "→ Committing…"
git -c user.email="Sindhuja.Sivaraman@htcinc.com" \
    -c user.name="Sindhuja.Sivaraman" \
    add -A
git -c user.email="Sindhuja.Sivaraman@htcinc.com" \
    -c user.name="Sindhuja.Sivaraman" \
    commit -m "Deploy $(date -u +%Y-%m-%dT%H:%M:%SZ)" || echo "  (nothing to commit — files identical)"

echo "→ Pushing to HF Space (this triggers the Docker build)…"
git push origin main 2>&1 | sed 's/^/  /'

echo
echo "✓ Push complete. The Space is now building."
echo
echo "Next:"
echo "  1. Watch the build:    https://huggingface.co/spaces/${SPACE}/logs"
echo "  2. Set secrets in:     https://huggingface.co/spaces/${SPACE}/settings"
echo "       FARADAY_LLM_CONFIG__API_KEY = <your-ollama-cloud-key>"
echo "       FARADAY_CORS_ORIGINS         = https://faraday-eta.vercel.app,https://*.vercel.app"
echo "  3. Smoke test once green:"
SPACE_URL_HOST="${SPACE//\//-}"
echo "       curl https://${SPACE_URL_HOST}.hf.space/health"
echo "       curl https://${SPACE_URL_HOST}.hf.space/health/llm"
echo
