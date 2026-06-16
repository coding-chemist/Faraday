"""Integration tests for engine/services/query_parser_service.py — real LLM.

Run with:  pytest -m llm  (requires Ollama running with qwen2.5:7b pulled, or
                           OLLAMA_HOST + OLLAMA_API_KEY set for Ollama Cloud)

Default pytest run skips these via the addopts = "-m 'not llm'" config.
"""
import pytest

from faraday_engine.factories.service_factory import ServiceFactory

pytestmark = pytest.mark.llm


@pytest.fixture(scope="module")
def parser():
    return ServiceFactory.create_query_parser_service()


def test_low_yield_suzuki_with_date_and_group(parser):
    spec = parser.parse(
        "Show Suzuki couplings where yield was below 70% in the last six months, colored by catalyst"
    )
    assert spec.reaction_type == "suzuki_coupling"
    assert spec.yield_max is not None and 60 <= spec.yield_max <= 80
    assert spec.date_from is not None
    assert spec.group_by == "catalyst"


def test_compare_amide_coupling_reagents(parser):
    spec = parser.parse("Compare HATU vs EDC amide coupling yields")
    assert spec.reaction_type == "amide_coupling"
    assert spec.chart_type == "bar"
    assert spec.aggregation in {"mean", "median"}


def test_average_yield_by_reaction_type_this_year(parser):
    spec = parser.parse("Average yield by reaction type this year")
    assert spec.group_by == "reaction_type"
    assert spec.aggregation == "mean"
    assert spec.metric == "yield_pct"
    assert spec.chart_type == "bar"


def test_failed_buchwald_reactions(parser):
    spec = parser.parse("Show failed Buchwald reactions")
    assert spec.reaction_type == "buchwald_hartwig"
    assert spec.status == "failed"


def test_yield_trends_over_time(parser):
    spec = parser.parse("Yield trends over the last year")
    assert spec.chart_type == "timeseries"
    assert spec.group_by == "month"


def test_high_yield_reactions_list(parser):
    spec = parser.parse("Show reactions above 90% yield")
    assert spec.yield_min is not None and 85 <= spec.yield_min <= 95


def test_distribution_of_yields(parser):
    spec = parser.parse("Distribution of yields across all reactions")
    assert spec.chart_type == "histogram"
    assert spec.metric == "yield_pct"


def test_most_common_solvent(parser):
    spec = parser.parse("Most common solvent in completed reactions")
    assert spec.status == "completed"
    assert spec.group_by == "solvent"


def test_suzukis_grouped_by_solvent(parser):
    spec = parser.parse("Suzukis in toluene vs dioxane")
    assert spec.reaction_type == "suzuki_coupling"
    assert spec.group_by == "solvent"


def test_intent_is_populated(parser):
    spec = parser.parse("any random query about reactions")
    assert spec.intent and len(spec.intent) >= 4


def test_heatmap_catalyst_by_solvent(parser):
    spec = parser.parse("Show yield by catalyst across solvents")
    assert spec.chart_type == "heatmap"
    assert spec.group_by in {"catalyst", "solvent"}
    assert spec.group_by_secondary in {"catalyst", "solvent"}
    assert spec.group_by != spec.group_by_secondary
