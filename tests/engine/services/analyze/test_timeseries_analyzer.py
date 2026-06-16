"""Tests for engine/services/analyze/timeseries_analyzer.py."""
from faraday_engine.domain.query_spec import Aggregation
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.timeseries_analyzer import TimeseriesAnalyzer


def _spec(**kwargs) -> QuerySpec:
    return QuerySpec(intent="test", chart_type=ChartType.TIMESERIES, **kwargs)


def test_buckets_by_month_no_group(df):
    data = TimeseriesAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.NONE, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
    )
    months = {p.x for p in data.points}
    assert all(isinstance(m, str) and "-" in m for m in months)
    # 7 distinct months for the 7 experiments with non-null yield
    assert len(months) == 7


def test_series_set_when_group_by_provided(df):
    data = TimeseriesAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.CATALYST, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
    )
    series_names = {p.series for p in data.points if p.series}
    assert "Pd(OAc)2" in series_names


def test_points_sorted_chronologically(df):
    data = TimeseriesAnalyzer().analyze(
        df,
        _spec(group_by=GroupBy.NONE, aggregation=Aggregation.MEAN, metric=Metric.YIELD_PCT),
    )
    xs = [p.x for p in data.points]
    assert xs == sorted(xs)
