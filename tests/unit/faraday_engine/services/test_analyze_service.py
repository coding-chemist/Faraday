"""Tests for engine/services/analyze_service.py — orchestration + registry dispatch.

Per-analyzer assertions live in tests/engine/services/analyze/test_*_analyzer.py.
These tests cover what AnalyzeService owns: the dispatch loop, summary card composition,
matched-experiment shaping, and intent passthrough.
"""
from datetime import datetime
from datetime import timedelta

import pytest

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType
from faraday_engine.domain.experiment import Reagent
from faraday_engine.domain.experiment import ReagentRole
from faraday_engine.domain.experiment import Result
from faraday_engine.domain.query_spec import Aggregation
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze_service import AnalyzeService


def _experiment(catalyst: str, solvent: str, yield_pct: float | None) -> Experiment:
    return Experiment(
        title=f"{catalyst} in {solvent}",
        type=ExperimentType.SUZUKI_COUPLING,
        status=ExperimentStatus.COMPLETED,
        solvent_name=solvent,
        started_at=datetime(2026, 3, 1, 9, 0),
        completed_at=datetime(2026, 3, 1, 21, 0),
        reagents=[
            Reagent(name=catalyst, role=ReagentRole.CATALYST, cas="3375-31-3", mw=224.51),
        ],
        result=Result(yield_pct=yield_pct) if yield_pct is not None else None,
    )


@pytest.fixture
def small_experiments() -> list[Experiment]:
    return [
        _experiment("Pd(OAc)2", "toluene", 85),
        _experiment("Pd(OAc)2", "dioxane", 72),
        _experiment("Pd(PPh3)4", "toluene", 45),
    ]


@pytest.fixture
def service() -> AnalyzeService:
    return AnalyzeService()


def _spec(chart_type: ChartType = ChartType.SCATTER, **kwargs) -> QuerySpec:
    return QuerySpec(intent="test", chart_type=chart_type, **kwargs)


def test_intent_echoed_from_spec(service, small_experiments):
    spec = QuerySpec(intent="Show me low yields", chart_type=ChartType.SCATTER)
    result = service.analyze(spec, small_experiments)
    assert result.intent == "Show me low yields"


def test_total_matched_reflects_input_count(service, small_experiments):
    result = service.analyze(_spec(), small_experiments)
    assert result.total_matched == 3


def test_matched_experiments_extract_catalyst(service, small_experiments):
    result = service.analyze(_spec(ChartType.LIST), small_experiments)
    pd_oac2 = [m for m in result.matched_experiments if m.catalyst == "Pd(OAc)2"]
    assert len(pd_oac2) == 2


def test_matched_experiments_preserve_solvent(service, small_experiments):
    result = service.analyze(_spec(ChartType.LIST), small_experiments)
    solvents = {m.solvent for m in result.matched_experiments}
    assert solvents == {"toluene", "dioxane"}


def test_registry_dispatches_to_every_chart_type(service, small_experiments):
    """Smoke test — analyze must succeed for every ChartType in the enum."""
    for chart_type in ChartType:
        if chart_type == ChartType.HEATMAP:
            spec = _spec(
                chart_type,
                group_by=GroupBy.CATALYST,
                group_by_secondary=GroupBy.SOLVENT,
                aggregation=Aggregation.MEAN,
                metric=Metric.YIELD_PCT,
            )
        else:
            spec = _spec(chart_type, group_by=GroupBy.CATALYST, metric=Metric.YIELD_PCT)
        result = service.analyze(spec, small_experiments)
        assert isinstance(result.chart_data, ChartData)
        assert result.chart_data.chart_type == chart_type.value


def test_empty_experiments_does_not_crash_any_chart_type(service):
    for chart_type in ChartType:
        if chart_type == ChartType.HEATMAP:
            spec = _spec(
                chart_type,
                group_by=GroupBy.CATALYST,
                group_by_secondary=GroupBy.SOLVENT,
                metric=Metric.YIELD_PCT,
            )
        else:
            spec = _spec(chart_type, metric=Metric.YIELD_PCT)
        result = service.analyze(spec, [])
        assert result.total_matched == 0
        assert result.matched_experiments == []
