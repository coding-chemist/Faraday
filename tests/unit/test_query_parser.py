"""Unit tests for QueryParserService — no LLM, no network."""
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
from faraday_engine.services.query_parser_service import QueryParserService
from tests.fakes.fake_llm import FakeLLMProvider


@pytest.fixture
def canned_spec() -> QuerySpec:
    """A baseline valid QuerySpec returned by the fake LLM."""
    return QuerySpec(
        reaction_type=ExperimentType.SUZUKI_COUPLING,
        yield_max=70.0,
        chart_type=ChartType.SCATTER,
        group_by=GroupBy.CATALYST,
        aggregation=Aggregation.COUNT,
        metric="yield_pct",
        intent="test intent",
    )


def test_prompt_includes_injected_today_date(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    service = QueryParserService(llm=fake_llm, today=datetime(2026, 6, 16))
    service.parse("show me anything")
    prompt = fake_llm.prompts_received[0]
    assert "2026-06-16" in prompt


def test_prompt_includes_user_query(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    service = QueryParserService(llm=fake_llm)
    service.parse("show Suzuki couplings")
    assert "show Suzuki couplings" in fake_llm.prompts_received[0]


def test_prompt_lists_every_reaction_type(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("test")
    prompt = fake_llm.prompts_received[0]
    for t in ExperimentType:
        assert t.value in prompt, f"reaction_type {t.value} missing from prompt"


def test_prompt_lists_every_status(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("test")
    prompt = fake_llm.prompts_received[0]
    for s in ExperimentStatus:
        assert s.value in prompt


def test_prompt_lists_every_chart_type(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("test")
    prompt = fake_llm.prompts_received[0]
    for c in ChartType:
        assert c.value in prompt


def test_prompt_lists_every_metric(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("test")
    prompt = fake_llm.prompts_received[0]
    for m in Metric:
        assert m.value in prompt


def test_returns_spec_from_llm_unchanged(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    service = QueryParserService(llm=fake_llm)
    result = service.parse("any query")
    assert result.reaction_type == ExperimentType.SUZUKI_COUPLING.value
    assert result.yield_max == 70.0
    assert result.chart_type == ChartType.SCATTER.value
    assert result.group_by == GroupBy.CATALYST.value


def test_service_resolves_today_lazily_when_unset(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    """Service with today=None should use utcnow() at call time, not import time."""
    fake_llm.canned_response = canned_spec
    service = QueryParserService(llm=fake_llm)
    service.parse("query")
    today_iso = datetime.utcnow().date().isoformat()
    assert today_iso in fake_llm.prompts_received[0]


# --- QuerySpec validator tests (no LLM needed at all) ---

def test_query_spec_rejects_yield_min_above_max():
    with pytest.raises(ValidationError, match="yield_min cannot exceed yield_max"):
        QuerySpec(yield_min=80, yield_max=50, intent="invalid")


def test_query_spec_rejects_date_from_after_date_to():
    with pytest.raises(ValidationError, match="date_from cannot be after date_to"):
        QuerySpec(
            date_from=datetime(2026, 6, 1),
            date_to=datetime(2026, 1, 1),
            intent="invalid",
        )


def test_query_spec_rejects_yield_out_of_range():
    with pytest.raises(ValidationError):
        QuerySpec(yield_min=150, intent="invalid")


def test_query_spec_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        QuerySpec(intent="test", unknown_field="anything")


def test_query_spec_defaults_are_sensible():
    spec = QuerySpec(intent="just a list")
    assert spec.chart_type == ChartType.SCATTER.value
    assert spec.group_by == GroupBy.NONE.value
    assert spec.group_by_secondary == GroupBy.NONE.value
    assert spec.aggregation == Aggregation.COUNT.value
    assert spec.metric == Metric.YIELD_PCT.value


# --- Heatmap-specific validation ---

def test_heatmap_requires_both_group_by_dims():
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


def test_non_heatmap_normalizes_group_by_secondary_to_none():
    """A non-heatmap chart with group_by_secondary set should silently normalize to NONE,
    not error — keeps the analyzer/renderer simple."""
    spec = QuerySpec(
        intent="bar chart, secondary should be ignored",
        chart_type=ChartType.BAR,
        group_by=GroupBy.CATALYST,
        group_by_secondary=GroupBy.SOLVENT,
    )
    assert spec.group_by_secondary == GroupBy.NONE.value
