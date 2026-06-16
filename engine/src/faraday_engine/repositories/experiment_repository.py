"""ExperimentRepository — class.verb shape. Owns Experiment + its child entities.

Filter rules are declarative — adding a new filter is one FilterRule entry, not a
new if/elif block in list().
"""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentFilters
from faraday_engine.domain.experiment import Reagent
from faraday_engine.domain.experiment import ReagentRole
from faraday_engine.domain.experiment import Result
from faraday_engine.repositories.filter_spec import FilterRule
from faraday_engine.repositories.filter_spec import apply_filter_rules
from faraday_engine.repositories.filter_spec import eq
from faraday_engine.repositories.filter_spec import ge
from faraday_engine.repositories.filter_spec import le
from faraday_engine.repositories.models import ExperimentORM
from faraday_engine.repositories.models import ReagentORM
from faraday_engine.repositories.models import ResultORM
from faraday_shared.logging import get_logger

log = get_logger(__name__)


# Declarative filter rules — to add a filter, add a row here and a field to
# ExperimentFilters. No changes to list() needed.
_EXPERIMENT_FILTER_RULES: list[FilterRule] = [
    FilterRule("type", ExperimentORM.type, eq, transform=lambda v: v.value),
    FilterRule("status", ExperimentORM.status, eq, transform=lambda v: v.value),
    FilterRule("solvent_name", ExperimentORM.solvent_name, eq),
    FilterRule("date_from", ExperimentORM.created_at, ge),
    FilterRule("date_to", ExperimentORM.created_at, le),
    FilterRule("yield_min", ResultORM.yield_pct, ge, join=ResultORM),
    FilterRule("yield_max", ResultORM.yield_pct, le, join=ResultORM),
    FilterRule(
        "catalyst_name",
        ReagentORM.name,
        eq,
        join=ExperimentORM.reagents,
        extra_where=(ReagentORM.role == ReagentRole.CATALYST.value),
    ),
]


class ExperimentRepository:
    """Data access for experiments. Verbs: create, fetch, list, update, delete."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, experiment: Experiment) -> Experiment:
        orm = self._to_orm(experiment)
        self._session.add(orm)
        self._session.flush()
        log.info("experiment.repo.create", id=orm.id, title=orm.title)
        return self._to_domain(orm)

    def fetch(self, id: str) -> Experiment | None:
        orm = self._session.get(ExperimentORM, id)
        return self._to_domain(orm) if orm else None

    def list(self, filters: ExperimentFilters | None = None) -> list[Experiment]:
        filters = filters or ExperimentFilters()
        stmt = select(ExperimentORM)
        stmt = apply_filter_rules(stmt, filters, _EXPERIMENT_FILTER_RULES)
        stmt = stmt.order_by(ExperimentORM.created_at.desc())
        stmt = stmt.limit(filters.limit).offset(filters.offset)
        orms = self._session.scalars(stmt).unique().all()
        return [self._to_domain(o) for o in orms]

    def update(self, id: str, data: dict) -> Experiment:
        orm = self._session.get(ExperimentORM, id)
        if orm is None:
            raise KeyError(f"Experiment not found: {id}")
        for key, value in data.items():
            if hasattr(orm, key) and key not in {"id", "reagents", "result", "created_at"}:
                setattr(orm, key, value)
        orm.updated_at = datetime.utcnow()
        self._session.flush()
        log.info("experiment.repo.update", id=id, fields=list(data.keys()))
        return self._to_domain(orm)

    def delete(self, id: str) -> None:
        orm = self._session.get(ExperimentORM, id)
        if orm is None:
            return
        self._session.delete(orm)
        log.info("experiment.repo.delete", id=id)

    def count_total(self) -> int:
        """Unfiltered count — used by /ask to show 'of N total' next to matched count."""
        return int(self._session.scalar(select(func.count(ExperimentORM.id))) or 0)

    # --- ORM ↔ domain conversion ---

    @staticmethod
    def _to_orm(exp: Experiment) -> ExperimentORM:
        orm = ExperimentORM(
            id=exp.id,
            title=exp.title,
            type=exp.type,
            status=exp.status,
            solvent_name=exp.solvent_name,
            temperature_c=exp.temperature_c,
            time_min=exp.time_min,
            atmosphere=exp.atmosphere,
            notes=exp.notes,
            started_at=exp.started_at,
            completed_at=exp.completed_at,
            created_at=exp.created_at,
            updated_at=exp.updated_at,
        )
        orm.reagents = [
            ReagentORM(
                id=r.id,
                experiment_id=exp.id,
                name=r.name,
                role=r.role,
                cas=r.cas,
                mw=r.mw,
                equivalents=r.equivalents,
                mass_g=r.mass_g,
                moles_mmol=r.moles_mmol,
                supplier=r.supplier,
                lot_number=r.lot_number,
                coa_url=r.coa_url,
            )
            for r in exp.reagents
        ]
        if exp.result is not None:
            orm.result = ResultORM(
                id=exp.result.id,
                experiment_id=exp.id,
                yield_pct=exp.result.yield_pct,
                purity_pct=exp.result.purity_pct,
                mass_g=exp.result.mass_g,
                moles_mmol=exp.result.moles_mmol,
                notes=exp.result.notes,
            )
        return orm

    @staticmethod
    def _to_domain(orm: ExperimentORM) -> Experiment:
        return Experiment(
            id=orm.id,
            title=orm.title,
            type=orm.type,
            status=orm.status,
            solvent_name=orm.solvent_name,
            temperature_c=orm.temperature_c,
            time_min=orm.time_min,
            atmosphere=orm.atmosphere,
            notes=orm.notes,
            started_at=orm.started_at,
            completed_at=orm.completed_at,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            reagents=[Reagent.model_validate(r) for r in orm.reagents],
            result=Result.model_validate(orm.result) if orm.result else None,
        )
