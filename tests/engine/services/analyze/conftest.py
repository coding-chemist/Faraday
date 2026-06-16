"""Shared fixtures for analyzer tests — 8 experiments spanning catalysts, solvents, yields."""
from datetime import datetime
from datetime import timedelta

import pytest

from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType
from faraday_engine.domain.experiment import Reagent
from faraday_engine.domain.experiment import ReagentRole
from faraday_engine.domain.experiment import Result
from faraday_engine.services.analyze.dataframe import experiments_to_dataframe


def _make(
    *,
    title: str,
    yield_pct: float | None,
    catalyst: str,
    solvent: str,
    started_at: datetime,
    type: ExperimentType = ExperimentType.SUZUKI_COUPLING,
    status: ExperimentStatus = ExperimentStatus.COMPLETED,
) -> Experiment:
    return Experiment(
        title=title,
        type=type,
        status=status,
        solvent_name=solvent,
        temperature_c=90.0,
        time_min=720,
        started_at=started_at,
        completed_at=started_at + timedelta(hours=12),
        reagents=[
            Reagent(name=catalyst, role=ReagentRole.CATALYST, cas="3375-31-3", mw=224.51),
            Reagent(name="potassium carbonate", role=ReagentRole.BASE, cas="584-08-7", mw=138.21),
            Reagent(name=solvent, role=ReagentRole.SOLVENT, cas="0", mw=0.0),
        ],
        result=Result(yield_pct=yield_pct, purity_pct=95.0) if yield_pct is not None else None,
    )


@pytest.fixture
def experiments() -> list[Experiment]:
    """8 fixture experiments — yields chosen so aggregation results are easy to verify by hand."""
    base = datetime(2026, 3, 1, 9, 0)
    return [
        _make(title="exp 1", yield_pct=85, catalyst="Pd(OAc)2", solvent="toluene",
              started_at=base + timedelta(days=0)),
        _make(title="exp 2", yield_pct=72, catalyst="Pd(OAc)2", solvent="dioxane",
              started_at=base + timedelta(days=30)),
        _make(title="exp 3", yield_pct=45, catalyst="Pd(PPh3)4", solvent="toluene",
              started_at=base + timedelta(days=60)),
        _make(title="exp 4", yield_pct=92, catalyst="Pd(dppf)Cl2", solvent="dioxane",
              started_at=base + timedelta(days=90)),
        _make(title="exp 5", yield_pct=68, catalyst="Pd(OAc)2", solvent="toluene",
              started_at=base + timedelta(days=120)),
        _make(title="exp 6", yield_pct=30, catalyst="Pd(PPh3)4", solvent="dioxane",
              started_at=base + timedelta(days=150)),
        _make(title="exp 7", yield_pct=88, catalyst="Pd(dppf)Cl2", solvent="toluene",
              started_at=base + timedelta(days=180)),
        _make(title="exp 8", yield_pct=None, catalyst="Pd(OAc)2", solvent="dioxane",
              started_at=base + timedelta(days=210), status=ExperimentStatus.IN_PROGRESS),
    ]


@pytest.fixture
def df(experiments):
    """The DataFrame analyzers consume directly."""
    return experiments_to_dataframe(experiments)
