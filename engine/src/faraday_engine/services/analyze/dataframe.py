"""Experiment list → flat pandas DataFrame.

Denormalizes catalyst/base into top-level columns so analyzers can group on them
without re-walking the nested reagents list. One row per experiment.
"""
from typing import Any

import pandas as pd

from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ReagentRole


_COLUMNS: list[str] = [
    "id",
    "title",
    "reaction_type",
    "status",
    "started_at",
    "completed_at",
    "month",
    "yield_pct",
    "purity_pct",
    "temperature_c",
    "time_min",
    "solvent",
    "catalyst",
    "base",
]


def experiments_to_dataframe(experiments: list[Experiment]) -> pd.DataFrame:
    """Build the canonical DataFrame the analyzers consume."""
    if not experiments:
        return pd.DataFrame(columns=_COLUMNS)

    rows: list[dict[str, Any]] = []
    for exp in experiments:
        catalyst = _first_role(exp, ReagentRole.CATALYST)
        base = _first_role(exp, ReagentRole.BASE)
        rows.append({
            "id": exp.id,
            "title": exp.title,
            "reaction_type": exp.type,
            "status": exp.status,
            "started_at": exp.started_at,
            "completed_at": exp.completed_at,
            "month": exp.started_at.strftime("%Y-%m") if exp.started_at else None,
            "yield_pct": exp.result.yield_pct if exp.result else None,
            "purity_pct": exp.result.purity_pct if exp.result else None,
            "temperature_c": exp.temperature_c,
            "time_min": exp.time_min,
            "solvent": exp.solvent_name,
            "catalyst": catalyst,
            "base": base,
        })
    return pd.DataFrame(rows, columns=_COLUMNS)


def _first_role(exp: Experiment, role: ReagentRole) -> str | None:
    for r in exp.reagents:
        if r.role == role.value:
            return r.name
    return None
