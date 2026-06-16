"""Unit tests for AnalyzeService — pure data shaping, no LLM, no DB."""
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


def _make_experiment(
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
    """8 fixture experiments — varied catalysts, solvents, yields, dates."""
    base = datetime(2026, 3, 1, 9, 0)
    return [
        _make_experiment(title="exp 1", yield_pct=85, catalyst="Pd(OAc)2", solvent="toluene",
                         started_at=base + timedelta(days=0)),
        _make_experiment(title="exp 2", yield_pct=72, catalyst="Pd(OAc)2", solvent="dioxane",
                         started_at=base + timedelta(days=30)),
        _make_experiment(title="exp 3", yield_pct=45, catalyst="Pd(PPh3)4", solvent="toluene",
                         started_at=base + timedelta(days=60)),
        _make_experiment(title="exp 4", yield_pct=92, catalyst="Pd(dppf)Cl2", solvent="dioxane",
                         started_at=base + timedelta(days=90)),
        _make_experiment(title="exp 5", yield_pct=68, catalyst="Pd(OAc)2", solvent="toluene",
                         started_at=base + timedelta(days=120)),
        _make_experiment(title="exp 6", yield_pct=30, catalyst="Pd(PPh3)4", solvent="dioxane",
                         started_at=base + timedelta(days=150)),
        _make_experiment(title="exp 7", yield_pct=88, catalyst="Pd(dppf)Cl2", solvent="toluene",
                         started_at=base + timedelta(days=180)),
        _make_experiment(title="exp 8", yield_pct=None, catalyst="Pd(OAc)2", solvent="dioxane",
                         started_at=base + timedelta(days=210), status=ExperimentStatus.IN_PROGRESS),
    ]


@pytest.fixture
def service() -> AnalyzeService:
    return AnalyzeService()


def _spec(chart_type: ChartType, **kwargs) -> QuerySpec:
    return QuerySpec(intent="test", chart_type=chart_type, **kwargs)


# --- Scatter ---

def test_scatter_emits_one_point_per_experiment_with_yield(service, experiments):
    result = service.analyze(
        _spec(ChartType.SCATTER, group_by=GroupBy.CATALYST, metric=Metric.YIELD_PCT),
        experiments,
    )
    assert result.chart_data.chart_type == ChartType.SCATTER.value
    # 7 of 8 have yield_pct
    assert len(result.chart_data.points) == 7
    # Color set from catalyst
    colors = {p.color for p in result.chart_data.points}
    assert colors == {"Pd(OAc)2", "Pd(PPh3)4", "Pd(dppf)Cl2"}
    # All points carry experiment id for click-through
    assert all(p.id for p in result.chart_data.points)


def test_scatter_with_no_group_by_omits_color(service, experiments):
    result = service.analyze(
        _spec(ChartType.SCATTER, group_by=GroupBy.NONE, metric=Metric.YIELD_PCT),
        experiments,
    )
    assert all(p.color is None for p in result.chart_data.points)


# --- Bar ---

def test_bar_aggregates_mean_yield_by_catalyst(service, experiments):
    result = service.analyze(
        _spec(
            ChartType.BAR,
            group_by=GroupBy.CATALYST,
            aggregation=Aggregation.MEAN,
            metric=Metric.YIELD_PCT,
        ),
        experiments,
    )
    assert result.chart_data.chart_type == ChartType.BAR.value
    by_catalyst = {p.x: p.y for p in result.chart_data.points}
    assert set(by_catalyst.keys()) == {"Pd(OAc)2", "Pd(PPh3)4", "Pd(dppf)Cl2"}
    # Pd(OAc)2: yields 85, 72, 68 → 75.0 (exp 8 has no yield, excluded)
    assert by_catalyst["Pd(OAc)2"] == pytest.approx(75.0, abs=0.1)
    # Pd(PPh3)4: 45, 30 → 37.5
    assert by_catalyst["Pd(PPh3)4"] == pytest.approx(37.5, abs=0.1)
    # Pd(dppf)Cl2: 92, 88 → 90.0
    assert by_catalyst["Pd(dppf)Cl2"] == pytest.approx(90.0, abs=0.1)


def test_bar_with_no_group_by_returns_single_total_bar(service, experiments):
    result = service.analyze(
        _spec(ChartType.BAR, group_by=GroupBy.NONE, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
        experiments,
    )
    assert len(result.chart_data.points) == 1
    assert result.chart_data.points[0].x == "all"


# --- Timeseries ---

def test_timeseries_buckets_by_month(service, experiments):
    result = service.analyze(
        _spec(
            ChartType.TIMESERIES,
            group_by=GroupBy.NONE,
            aggregation=Aggregation.MEAN,
            metric=Metric.YIELD_PCT,
        ),
        experiments,
    )
    assert result.chart_data.chart_type == ChartType.TIMESERIES.value
    months = {p.x for p in result.chart_data.points}
    assert all(isinstance(m, str) and "-" in m for m in months)
    # 7 distinct months for the 7 experiments with yields
    assert len(months) == 7


def test_timeseries_series_set_by_group_by(service, experiments):
    result = service.analyze(
        _spec(
            ChartType.TIMESERIES,
            group_by=GroupBy.CATALYST,
            aggregation=Aggregation.MEAN,
            metric=Metric.YIELD_PCT,
        ),
        experiments,
    )
    series = {p.series for p in result.chart_data.points}
    assert "Pd(OAc)2" in series


# --- Histogram ---

def test_histogram_produces_ten_bins(service, experiments):
    result = service.analyze(
        _spec(ChartType.HISTOGRAM, metric=Metric.YIELD_PCT),
        experiments,
    )
    assert result.chart_data.chart_type == ChartType.HISTOGRAM.value
    assert len(result.chart_data.histogram_bins) == 10
    total = sum(b.count for b in result.chart_data.histogram_bins)
    assert total == 7  # 7 of 8 experiments have yield_pct


# --- Heatmap ---

def test_heatmap_pivots_catalyst_by_solvent(service, experiments):
    result = service.analyze(
        _spec(
            ChartType.HEATMAP,
            group_by=GroupBy.CATALYST,
            group_by_secondary=GroupBy.SOLVENT,
            aggregation=Aggregation.MEAN,
            metric=Metric.YIELD_PCT,
        ),
        experiments,
    )
    assert result.chart_data.chart_type == ChartType.HEATMAP.value
    cells = {(c.x, c.y): c for c in result.chart_data.heatmap_cells}
    # Pd(OAc)2 × toluene: 85, 68 → 76.5
    assert cells[("Pd(OAc)2", "toluene")].value == pytest.approx(76.5, abs=0.1)
    # Pd(PPh3)4 × dioxane: 30 only
    assert cells[("Pd(PPh3)4", "dioxane")].value == pytest.approx(30.0, abs=0.1)


# --- List ---

def test_list_returns_no_chart_points_only_matched(service, experiments):
    result = service.analyze(_spec(ChartType.LIST), experiments)
    assert result.chart_data.chart_type == ChartType.LIST.value
    assert result.chart_data.points == []
    assert len(result.matched_experiments) == 8


# --- Summary cards ---

def test_summary_cards_include_count_avg_mode(service, experiments):
    result = service.analyze(_spec(ChartType.SCATTER), experiments, total_in_db=210)
    labels = {c.label for c in result.summary_cards}
    assert "Matched experiments" in labels
    assert "Average yield" in labels
    assert "Most common catalyst" in labels
    matched_card = next(c for c in result.summary_cards if c.label == "Matched experiments")
    assert matched_card.value == "8"
    assert matched_card.sublabel == "of 210 total"


def test_summary_cards_when_empty_returns_zero_only(service):
    result = service.analyze(_spec(ChartType.SCATTER), [])
    assert len(result.summary_cards) == 1
    assert result.summary_cards[0].value == "0"


def test_worst_yield_card_appears_when_yield_below_50(service, experiments):
    """Fixture has yields of 30 and 45 — worst yield card should appear."""
    result = service.analyze(_spec(ChartType.SCATTER), experiments)
    labels = {c.label for c in result.summary_cards}
    assert "Worst yield" in labels


# --- AnalysisResult shape ---

def test_intent_echoed_from_spec(service, experiments):
    spec = QuerySpec(intent="Show me low yields", chart_type=ChartType.SCATTER)
    result = service.analyze(spec, experiments)
    assert result.intent == "Show me low yields"


def test_total_matched_reflects_input(service, experiments):
    result = service.analyze(_spec(ChartType.SCATTER), experiments)
    assert result.total_matched == 8


def test_matched_experiments_have_catalyst_extracted(service, experiments):
    result = service.analyze(_spec(ChartType.LIST), experiments)
    pd_oac2_runs = [m for m in result.matched_experiments if m.catalyst == "Pd(OAc)2"]
    assert len(pd_oac2_runs) == 4


# --- QuerySpec.to_filters() ---

def test_spec_to_filters_maps_all_fields():
    spec = QuerySpec(
        intent="test",
        reaction_type=ExperimentType.SUZUKI_COUPLING,
        status=ExperimentStatus.COMPLETED,
        catalyst_name="Pd(OAc)2",
        solvent_name="toluene",
        yield_min=50,
        yield_max=95,
        date_from=datetime(2026, 1, 1),
        date_to=datetime(2026, 6, 1),
    )
    filters = spec.to_filters()
    assert filters.type == ExperimentType.SUZUKI_COUPLING.value
    assert filters.status == ExperimentStatus.COMPLETED.value
    assert filters.catalyst_name == "Pd(OAc)2"
    assert filters.solvent_name == "toluene"
    assert filters.yield_min == 50
    assert filters.yield_max == 95
    assert filters.limit == 10_000


# --- Registry introspection ---

def test_all_six_chart_types_are_registered(service, experiments):
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
        result = service.analyze(spec, experiments)
        assert isinstance(result.chart_data, ChartData)
        assert result.chart_data.chart_type == chart_type.value
