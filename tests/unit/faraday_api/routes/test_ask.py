"""Unit tests for apps/api/routes/ask.py — uses dependency_overrides, no LLM, no DB."""
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from faraday_api.deps import get_analyze_service
from faraday_api.deps import get_experiment_service
from faraday_api.deps import get_query_parser_service
from faraday_api.main import app
from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType
from faraday_engine.domain.experiment import Reagent
from faraday_engine.domain.experiment import ReagentRole
from faraday_engine.domain.experiment import Result
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze_service import AnalyzeService


def _experiment(catalyst: str, yield_pct: float) -> Experiment:
    return Experiment(
        title=f"test {catalyst}",
        type=ExperimentType.SUZUKI_COUPLING,
        status=ExperimentStatus.COMPLETED,
        solvent_name="toluene",
        started_at=datetime(2026, 3, 1, 9, 0),
        completed_at=datetime(2026, 3, 1, 21, 0),
        reagents=[
            Reagent(name=catalyst, role=ReagentRole.CATALYST, cas="3375-31-3", mw=224.51),
        ],
        result=Result(yield_pct=yield_pct),
    )


class _FakeParser:
    def __init__(self, spec: QuerySpec):
        self._spec = spec
        self.calls: list[str] = []

    def parse(self, query: str) -> QuerySpec:
        self.calls.append(query)
        return self._spec


class _FakeExperimentService:
    def __init__(self, experiments: list[Experiment], total: int):
        self._experiments = experiments
        self._total = total
        self.list_calls: list = []

    def list(self, filters):
        self.list_calls.append(filters)
        return self._experiments

    def count_total(self) -> int:
        return self._total


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def fake_parser():
    spec = QuerySpec(
        reaction_type=ExperimentType.SUZUKI_COUPLING,
        yield_max=80.0,
        chart_type=ChartType.BAR,
        group_by=GroupBy.CATALYST,
        intent="Suzuki couplings yield below 80% by catalyst",
    )
    return _FakeParser(spec)


@pytest.fixture
def fake_experiments():
    return _FakeExperimentService(
        experiments=[
            _experiment("Pd(OAc)2", 75),
            _experiment("Pd(OAc)2", 68),
            _experiment("Pd(PPh3)4", 42),
        ],
        total=210,
    )


@pytest.fixture(autouse=True)
def _override_deps(fake_parser, fake_experiments):
    app.dependency_overrides[get_query_parser_service] = lambda: fake_parser
    app.dependency_overrides[get_experiment_service] = lambda: fake_experiments
    app.dependency_overrides[get_analyze_service] = lambda: AnalyzeService()
    yield
    app.dependency_overrides.clear()


# --- Request validation ---

def test_rejects_empty_query(client):
    response = client.post("/memory/ask", json={"query": ""})
    assert response.status_code == 422


def test_rejects_query_below_min_length(client):
    response = client.post("/memory/ask", json={"query": "a"})
    assert response.status_code == 422


def test_rejects_missing_query_field(client):
    response = client.post("/memory/ask", json={})
    assert response.status_code == 422


# --- Happy path ---

def test_returns_200_with_analysis_result(client):
    response = client.post("/memory/ask", json={"query": "Show low-yield Suzukis by catalyst"})
    assert response.status_code == 200
    body = response.json()
    assert "chart_data" in body
    assert "summary_cards" in body
    assert "matched_experiments" in body
    assert body["total_matched"] == 3
    assert body["intent"] == "Suzuki couplings yield below 80% by catalyst"


def test_chart_type_in_response_matches_spec(client):
    response = client.post("/memory/ask", json={"query": "anything"})
    assert response.json()["chart_data"]["chart_type"] == "bar"


def test_summary_includes_of_total_subtext(client):
    response = client.post("/memory/ask", json={"query": "anything"})
    matched_card = next(
        c for c in response.json()["summary_cards"] if c["label"] == "Matched experiments"
    )
    assert matched_card["value"] == "3"
    assert matched_card["sublabel"] == "of 210 total"


def test_orchestration_calls_parser_then_lists(client, fake_parser, fake_experiments):
    client.post("/memory/ask", json={"query": "test query"})
    assert fake_parser.calls == ["test query"]
    assert len(fake_experiments.list_calls) == 1
    filters = fake_experiments.list_calls[0]
    assert filters.type == ExperimentType.SUZUKI_COUPLING.value
    assert filters.yield_max == 80.0


# --- Error path ---

def test_parser_failure_returns_422(client, fake_parser):
    def raise_parse(query):
        raise RuntimeError("LLM unreachable")

    fake_parser.parse = raise_parse
    response = client.post("/memory/ask", json={"query": "anything"})
    assert response.status_code == 422
    assert "Could not understand" in response.json()["detail"]


# --- Request tracing ---

def test_request_id_header_echoed(client):
    response = client.post(
        "/memory/ask",
        json={"query": "test"},
        headers={"x-request-id": "abc-123"},
    )
    assert response.headers["x-request-id"] == "abc-123"
