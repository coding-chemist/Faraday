"""Seed orchestrator — walks the SeederRegistry, generates experiments, persists via repository.

Each seeder registers itself on import. To add a new experiment type, drop a new
*_seeder.py file with @SeederRegistry.register(...) and add the import line below.
"""
from random import Random

from sqlalchemy import delete

from faraday_engine.domain.experiment import Experiment
from faraday_engine.repositories.experiment_repository import ExperimentRepository
from faraday_engine.repositories.models import ExperimentORM
from faraday_engine.repositories.session import session_scope
from faraday_engine.seed.base import ExperimentSeeder, SeederRegistry
from faraday_shared.logging import get_logger

# Importing each seeder triggers @SeederRegistry.register — keep imports explicit + greppable
from faraday_engine.seed.amide_coupling_seeder import AmideCouplingSeeder  # noqa: F401
from faraday_engine.seed.buchwald_seeder import BuchwaldSeeder  # noqa: F401
from faraday_engine.seed.reduction_seeder import CarbonylReductionSeeder  # noqa: F401
from faraday_engine.seed.reductive_amination_seeder import ReductiveAminationSeeder  # noqa: F401
from faraday_engine.seed.suzuki_seeder import SuzukiSeeder  # noqa: F401

log = get_logger(__name__)

__all__ = ["seed_database", "ExperimentSeeder", "SeederRegistry"]


def seed_database(
    seed: int = 42,
    clear: bool = False,
    counts: dict | None = None,
) -> dict[str, int]:
    """Generate and persist experiments via every registered seeder.

    Args:
        seed: RNG seed for reproducibility (default 42 → same dataset every run).
        clear: If True, delete all existing experiments before seeding.
        counts: Override per-type counts. {ExperimentType: int}. Defaults to each
                seeder's `default_count`.

    Returns:
        {experiment_type_value: count_persisted} summary.
    """
    rng = Random(seed)
    summary: dict[str, int] = {}

    with session_scope() as session:
        if clear:
            n = session.execute(delete(ExperimentORM)).rowcount
            log.info("seed.clear", removed=n)

        repository = ExperimentRepository(session)
        counts = counts or {}

        for experiment_type, seeder_cls, default_count in SeederRegistry.all():
            target = counts.get(experiment_type, default_count)
            if target <= 0:
                continue
            seeder = seeder_cls(rng)
            log.info("seed.type.start", type=experiment_type.value, target=target)
            for _ in range(target):
                experiment: Experiment = seeder.generate()
                repository.create(experiment)
            summary[experiment_type.value] = target
            log.info("seed.type.done", type=experiment_type.value, count=target)

    total = sum(summary.values())
    log.info("seed.complete", total=total, breakdown=summary)
    return summary
