"""Seeder base + registry. Each experiment type self-registers; orchestrator walks the registry."""
from abc import ABC, abstractmethod
from random import Random
from typing import ClassVar

from faraday_engine.domain.experiment import Experiment, ExperimentType


class ExperimentSeeder(ABC):
    """Generates one or more realistic experiments of a single type.

    Each concrete seeder owns its parameter space (catalysts, solvents, substrates,
    yield distribution shape) and registers via @SeederRegistry.register.
    """

    experiment_type: ClassVar[ExperimentType]
    default_count: ClassVar[int] = 25

    def __init__(self, rng: Random) -> None:
        self._rng = rng

    @abstractmethod
    def generate(self) -> Experiment:
        """Produce one experiment. Called `count` times by the orchestrator."""


class SeederRegistry:
    """Name -> (seeder_cls, default_count). Populated at import time."""

    _seeders: ClassVar[dict[ExperimentType, tuple[type[ExperimentSeeder], int]]] = {}

    @classmethod
    def register(cls, experiment_type: ExperimentType, count: int):
        """Decorator — each seeder self-registers with its type + default count."""
        def wrap(seeder_cls: type[ExperimentSeeder]) -> type[ExperimentSeeder]:
            if experiment_type in cls._seeders:
                raise ValueError(f"Seeder for {experiment_type} already registered")
            seeder_cls.experiment_type = experiment_type
            seeder_cls.default_count = count
            cls._seeders[experiment_type] = (seeder_cls, count)
            return seeder_cls
        return wrap

    @classmethod
    def resolve(cls, experiment_type: ExperimentType) -> tuple[type[ExperimentSeeder], int]:
        if experiment_type not in cls._seeders:
            raise ValueError(
                f"No seeder registered for {experiment_type}. "
                f"Available: {sorted(t.value for t in cls._seeders)}"
            )
        return cls._seeders[experiment_type]

    @classmethod
    def all(cls) -> list[tuple[ExperimentType, type[ExperimentSeeder], int]]:
        return [(t, scls, n) for t, (scls, n) in cls._seeders.items()]
