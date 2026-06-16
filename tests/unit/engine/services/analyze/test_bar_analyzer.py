"""Tests for engine/services/analyze/bar_analyzer.py."""
import pytest

from faraday_engine.domain.query_spec import Aggregation
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.bar_analyzer import BarAnalyzer


def _spec(**kwargs) -> QuerySpec:
    return QuerySpec(intent="test", chart_type=ChartType.BAR, **kwargs)


def test_mean_yield_by_catalyst(df):
    data = BarAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.CATALYST, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
    )
    by_catalyst = {p.x: p.y for p in data.points}
    assert set(by_catalyst.keys()) == {"Pd(OAc)2", "Pd(PPh3)4", "Pd(dppf)Cl2"}
    # Pd(OAc)2: 85, 72, 68 (exp 8 null excluded) → 75.0
    assert by_catalyst["Pd(OAc)2"] == pytest.approx(75.0, abs=0.1)
    # Pd(PPh3)4: 45, 30 → 37.5
    assert by_catalyst["Pd(PPh3)4"] == pytest.approx(37.5, abs=0.1)
    # Pd(dppf)Cl2: 92, 88 → 90.0
    assert by_catalyst["Pd(dppf)Cl2"] == pytest.approx(90.0, abs=0.1)


def test_no_group_by_returns_single_total_bar(df):
    data = BarAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.NONE, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
    )
    assert len(data.points) == 1
    assert data.points[0].x == "all"


def test_bars_sorted_by_value_descending(df):
    data = BarAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.CATALYST, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
    )
    values = [p.y for p in data.points]
    assert values == sorted(values, reverse=True)


def test_count_aggregation_counts_rows_per_group(df):
    data = BarAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.CATALYST, aggregation=Aggregation.COUNT, metric=Metric.YIELD_PCT),
    )
    by_catalyst = {p.x: p.y for p in data.points}
    # Pd(OAc)2 has 4 experiments (one with null yield_pct still counts toward the row total
    # if agg is count on the whole DF row, but here metric=yield_pct counts non-null)
    assert by_catalyst["Pd(OAc)2"] == 3.0  # 85, 72, 68 (exp 8 yield null)
