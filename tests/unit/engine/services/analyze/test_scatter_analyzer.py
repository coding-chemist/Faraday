"""Tests for engine/services/analyze/scatter_analyzer.py."""
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.scatter_analyzer import ScatterAnalyzer


def _spec(**kwargs) -> QuerySpec:
    return QuerySpec(intent="test", chart_type=ChartType.SCATTER, **kwargs)


def test_emits_one_point_per_experiment_with_yield(df):
    data = ScatterAnalyzer().analyze(df, _spec(group_by=GroupBy.CATALYST, metric=Metric.YIELD_PCT))
    # 7 of 8 fixture experiments have yield_pct
    assert len(data.points) == 7


def test_colors_set_from_group_by(df):
    data = ScatterAnalyzer().analyze(df, _spec(group_by=GroupBy.CATALYST, metric=Metric.YIELD_PCT))
    colors = {p.color for p in data.points}
    assert colors == {"Pd(OAc)2", "Pd(PPh3)4", "Pd(dppf)Cl2"}


def test_color_omitted_when_group_by_none(df):
    data = ScatterAnalyzer().analyze(df, _spec(group_by=GroupBy.NONE, metric=Metric.YIELD_PCT))
    assert all(p.color is None for p in data.points)


def test_each_point_carries_experiment_id_for_click_through(df):
    data = ScatterAnalyzer().analyze(df, _spec(group_by=GroupBy.CATALYST, metric=Metric.YIELD_PCT))
    assert all(p.id for p in data.points)
