"""End-to-end /ask test against real LLM + seeded DB.

Prereq:
  - Ollama running locally with qwen2.5:7b pulled
  - `make seed` has been run (or seed_database is auto-invoked here)

Run with:  pytest -m llm
"""
import pytest
from fastapi.testclient import TestClient

from faraday_api.main import app
from faraday_engine.repositories.session import init_db
from faraday_engine.repositories.session import session_scope
from faraday_engine.seed import seed_database

pytestmark = pytest.mark.llm


@pytest.fixture(scope="module", autouse=True)
def _seeded_db():
    """Ensure the DB has experiments before running these tests."""
    init_db()
    with session_scope() as session:
        from faraday_engine.repositories.models import ExperimentORM
        count = session.query(ExperimentORM).count()
    if count == 0:
        seed_database(seed=42)
    yield


@pytest.fixture
def client():
    return TestClient(app)


def test_canonical_low_yield_suzuki_query(client):
    response = client.post(
        "/ask",
        json={"query": "Show Suzuki couplings yield below 70% in last 6 months by catalyst"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total_matched"] > 0
    assert body["chart_data"]["chart_type"] in {"scatter", "bar"}
    # The intent should mention Suzuki and yield
    assert "suzuki" in body["intent"].lower() or "yield" in body["intent"].lower()


def test_compare_reagents_returns_bar_chart(client):
    response = client.post(
        "/ask",
        json={"query": "Compare HATU vs EDC amide coupling yields"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_data"]["chart_type"] == "bar"


def test_heatmap_query_returns_heatmap_cells(client):
    response = client.post(
        "/ask",
        json={"query": "Yield by catalyst across solvents"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_data"]["chart_type"] == "heatmap"
    assert len(body["chart_data"]["heatmap_cells"]) > 0
