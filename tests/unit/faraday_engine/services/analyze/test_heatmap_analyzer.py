"""Tests for engine/services/analyze/heatmap_analyzer.py."""
import pytest

from faraday_engine.domain.query_spec import Aggregation
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.heatmap_analyzer import HeatmapAnalyzer


def _spec(**kwargs) -> QuerySpec:
    return QuerySpec(
        intent="test",
        chart_type=ChartType.HEATMAP,
        group_by=GroupBy.CATALYST,
        group_by_secondary=GroupBy.SOLVENT,
        aggregation=Aggregation.MEAN,
        metric=Metric.YIELD_PCT,
        **kwargs,
    )


def test_pivots_catalyst_by_solvent(df):
    data = HeatmapAnalyzer().analyze(df, _spec())
    cells = {(c.x, c.y): c for c in data.heatmap_cells}
    # Pd(OAc)2 × toluene: 85, 68 → 76.5
    assert cells[("Pd(OAc)2", "toluene")].value == pytest.approx(76.5, abs=0.1)
    # Pd(PPh3)4 × dioxane: 30 only
    assert cells[("Pd(PPh3)4", "dioxane")].value == pytest.approx(30.0, abs=0.1)
    # Cell count carries the n behind each value
    assert cells[("Pd(OAc)2", "toluene")].count == 2


def test_axis_labels_set_from_group_by_dims(df):
    data = HeatmapAnalyzer().analyze(df, _spec())
    assert "Catalyst" in data.x_label
    assert "Solvent" in data.y_label
