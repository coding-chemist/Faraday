#!/bin/sh
# Faraday HF Spaces entrypoint.
#
# Runs once before supervisord starts:
#   1. init_db() — creates SQLite tables if missing (idempotent)
#   2. seed_database() — populates 210 experiments IF db is empty
#
# Then hands off to supervisord which runs redis + uvicorn + celery worker.

set -e

echo "[entrypoint] Initializing database…"
uv run --no-dev python <<'PY'
from faraday_engine.repositories.session import init_db, session_scope
from faraday_engine.repositories.models import ExperimentORM

init_db()
with session_scope() as session:
    count = session.query(ExperimentORM).count()

if count == 0:
    print("[seed] Database empty — seeding 210 experiments…")
    from faraday_engine.seed import seed_database
    summary = seed_database(seed=42)
    total = sum(summary.values())
    print(f"[seed] Done — {total} experiments inserted.")
else:
    print(f"[seed] Database already has {count} experiments — skipping seed.")
PY

echo "[entrypoint] Starting supervisord…"
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
