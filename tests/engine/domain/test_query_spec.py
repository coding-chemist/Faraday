"""Tests for engine/domain/query_spec.py — pure schema validation, no LLM."""
from datetime import datetime

import pytest
from pydantic import ValidationError

from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType
from faraday_engine.domain.query_spec import Aggregation
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec


def test_defaults_are_sensible():
    spec = QuerySpec(intent="just a list")
    assert spec.chart_type == ChartType.SCATTER.value
    assert spec.group_by == GroupBy.NONE.value
    assert spec.group_by_secondary == GroupBy.NONE.value
    assert spec.aggregation == Aggregation.COUNT.value
    assert spec.metric == Metric.YIELD_PCT.value


def test_rejects_yield_min_above_max():
    with pytest.raises(ValidationError, match="yield_min cannot exceed yield_max"):
        QuerySpec(yield_min=80, yield_max=50, intent="invalid")


def test_rejects_date_from_after_date_to():
    with pytest.raises(ValidationError, match="date_from cannot be after date_to"):
        QuerySpec(
            date_from=datetime(2026, 6, 1),
            date_to=datetime(2026, 1, 1),
            intent="invalid",
        )


def test_rejects_yield_out_of_range():
    with pytest.raises(ValidationError):
        QuerySpec(yield_min=150, intent="invalid")


def test_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        QuerySpec(intent="test", unknown_field="anything")


# --- Heatmap-specific validation ---

def test_heatmap_requires_both_group_dims():
    with pytest.raises(ValidationError, match="heatmap requires both group_by"):
        QuerySpec(
            intent="heatmap missing secondary",
            chart_type=ChartType.HEATMAP,
            group_by=GroupBy.CATALYST,
        )


def test_heatmap_requires_distinct_group_dims():
    with pytest.raises(ValidationError, match="must differ"):
        QuerySpec(
            intent="heatmap with same dims",
            chart_type=ChartType.HEATMAP,
            group_by=GroupBy.CATALYST,
            group_by_secondary=GroupBy.CATALYST,
        )


def test_heatmap_accepts_two_distinct_group_dims():
    spec = QuerySpec(
        intent="catalyst × solvent",
        chart_type=ChartType.HEATMAP,
        group_by=GroupBy.CATALYST,
        group_by_secondary=GroupBy.SOLVENT,
        aggregation=Aggregation.MEAN,
        metric=Metric.YIELD_PCT,
    )
    assert spec.chart_type == ChartType.HEATMAP.value
    assert spec.group_by == GroupBy.CATALYST.value
    assert spec.group_by_secondary == GroupBy.SOLVENT.value


def test_non_heatmap_normalizes_secondary_to_none():
    spec = QuerySpec(
        intent="bar chart, secondary should be ignored",
        chart_type=ChartType.BAR,
        group_by=GroupBy.CATALYST,
        group_by_secondary=GroupBy.SOLVENT,
    )
    assert spec.group_by_secondary == GroupBy.NONE.value


# --- to_filters() ---

def test_to_filters_maps_all_fields():
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


def test_to_filters_accepts_limit_override():
    spec = QuerySpec(intent="test")
    assert spec.to_filters(limit=50).limit == 50
