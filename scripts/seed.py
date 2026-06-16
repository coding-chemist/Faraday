"""CLI entrypoint for seeding the database.

Usage:
    uv run python scripts/seed.py                  # seed with default counts
    uv run python scripts/seed.py --clear          # wipe existing data first
    uv run python scripts/seed.py --seed 123       # different RNG seed
"""
import argparse
import sys

from faraday_engine.repositories.session import init_db
from faraday_engine.seed import seed_database
from faraday_shared.config import settings
from faraday_shared.logging import get_logger, setup_logging


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed Faraday's database with realistic experiments.")
    parser.add_argument("--clear", action="store_true", help="Delete all existing experiments first")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducible data (default 42)")
    args = parser.parse_args()

    setup_logging(level=settings.log_level, json=False)  # human-friendly for CLI
    log = get_logger("faraday.seed")

    init_db()
    log.info("seed.start", clear=args.clear, seed=args.seed)
    summary = seed_database(seed=args.seed, clear=args.clear)

    total = sum(summary.values())
    print(f"\nSeeded {total} experiments:")
    for t, n in sorted(summary.items()):
        print(f"  {t:30s} {n:4d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
