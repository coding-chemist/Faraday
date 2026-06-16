"""Tests for engine/services/analyze/histogram_analyzer.py."""
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.histogram_analyzer import HistogramAnalyzer


def _spec(**kwargs) -> QuerySpec:
    return QuerySpec(intent="test", chart_type=ChartType.HISTOGRAM, **kwargs)


def test_produces_ten_bins(df):
    data = HistogramAnalyzer().analyze(df, _spec(metric=Metric.YIELD_PCT))
    assert len(data.histogram_bins) == 10


def test_bin_counts_sum_to_non_null_metric_count(df):
    data = HistogramAnalyzer().analyze(df, _spec(metric=Metric.YIELD_PCT))
    total = sum(b.count for b in data.histogram_bins)
    assert total == 7  # 7 of 8 fixture experiments have yield_pct


def test_bins_are_contiguous(df):
    data = HistogramAnalyzer().analyze(df, _spec(metric=Metric.YIELD_PCT))
    for i in range(len(data.histogram_bins) - 1):
        assert data.histogram_bins[i].bin_high == data.histogram_bins[i + 1].bin_low
