"""Tests for engine/services/query_parser_service.py — uses FakeLLMProvider, no network."""
from datetime import datetime

import pytest

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
    return QuerySpec(
        reaction_type=ExperimentType.SUZUKI_COUPLING,
        yield_max=70.0,
        chart_type=ChartType.SCATTER,
        group_by=GroupBy.CATALYST,
        aggregation=Aggregation.COUNT,
        metric=Metric.YIELD_PCT,
        intent="test intent",
    )


def test_prompt_includes_injected_today_date(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    service = QueryParserService(llm=fake_llm, today=datetime(2026, 6, 16))
    service.parse("show me anything")
    assert "2026-06-16" in fake_llm.prompts_received[0]


def test_prompt_includes_user_query(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("show Suzuki couplings")
    assert "show Suzuki couplings" in fake_llm.prompts_received[0]


def test_prompt_lists_every_reaction_type(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("test")
    prompt = fake_llm.prompts_received[0]
    for t in ExperimentType:
        assert t.value in prompt


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
    result = QueryParserService(llm=fake_llm).parse("any query")
    assert result.reaction_type == ExperimentType.SUZUKI_COUPLING.value
    assert result.yield_max == 70.0
    assert result.chart_type == ChartType.SCATTER.value
    assert result.group_by == GroupBy.CATALYST.value


def test_today_resolves_lazily_when_unset(fake_llm: FakeLLMProvider, canned_spec: QuerySpec):
    fake_llm.canned_response = canned_spec
    QueryParserService(llm=fake_llm).parse("query")
    today_iso = datetime.utcnow().date().isoformat()
    assert today_iso in fake_llm.prompts_received[0]
