"""CLI for embedding backfill — synchronous, no Celery needed.

In production, the API queues `embedding.create` Celery tasks per new experiment. For
seed/dev convenience, this script runs the same backfill in-process.

Usage:
    uv run python scripts/embed.py            # backfill all experiments
"""
import sys

from faraday_engine.factories.service_factory import ServiceFactory
from faraday_engine.repositories.session import init_db
from faraday_engine.repositories.session import session_scope
from faraday_shared.config import settings
from faraday_shared.logging import get_logger
from faraday_shared.logging import setup_logging


def main() -> int:
    setup_logging(level=settings.log_level, json=False)
    log = get_logger("faraday.embed")

    init_db()
    log.info("embed.cli.start")

    with session_scope() as session:
        service = ServiceFactory.create_embedding_service(session)
        count = service.backfill()

    print(f"\nEmbedded {count} experiments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
