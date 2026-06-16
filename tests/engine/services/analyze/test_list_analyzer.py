"""Tests for engine/services/analyze/list_analyzer.py."""
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.list_analyzer import ListAnalyzer


def test_returns_empty_chart_data(df):
    spec = QuerySpec(intent="just a list", chart_type=ChartType.LIST)
    data = ListAnalyzer().analyze(df, spec)
    assert data.chart_type == ChartType.LIST.value
    assert data.points == []
    assert data.heatmap_cells == []
    assert data.histogram_bins == []
