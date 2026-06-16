"""Smoke-test the QueryParserService against the real LLM.

Useful for catching prompt drift early — type a query, see what the LLM returns.

Usage:
    uv run python scripts/parse_query.py "Show Suzuki couplings yield <70% last 6 months"
    uv run python scripts/parse_query.py "Compare HATU vs EDC amide coupling yields"
"""
import argparse
import sys

from faraday_engine.factories.service_factory import ServiceFactory
from faraday_shared.config import settings
from faraday_shared.logging import get_logger
from faraday_shared.logging import setup_logging


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse a natural-language query into a QuerySpec via the configured LLM provider.",
    )
    parser.add_argument("query", help="The natural-language query")
    args = parser.parse_args()

    setup_logging(level=settings.log_level, json=False)
    log = get_logger("faraday.parse_query")
    log.info("parse.cli.start", provider=settings.llm.provider)

    service = ServiceFactory.create_query_parser_service()
    spec = service.parse(args.query)

    print()
    print(spec.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
