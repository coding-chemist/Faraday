"""Tests for engine/services/analyze/summary.py."""
import pandas as pd

from faraday_engine.services.analyze.summary import build_summary_cards


def test_returns_zero_card_when_empty():
    cards = build_summary_cards(pd.DataFrame())
    assert len(cards) == 1
    assert cards[0].value == "0"


def test_includes_matched_count_with_total_subtext(df):
    cards = build_summary_cards(df, total_in_db=210)
    matched = next(c for c in cards if c.label == "Matched experiments")
    assert matched.value == "8"
    assert matched.sublabel == "of 210 total"


def test_average_yield_card_uses_mean_with_median_subtext(df):
    cards = build_summary_cards(df)
    avg_card = next(c for c in cards if c.label == "Average yield")
    assert "%" in avg_card.value
    assert avg_card.sublabel and "median" in avg_card.sublabel


def test_most_common_catalyst_card_uses_mode(df):
    cards = build_summary_cards(df)
    cat_card = next(c for c in cards if c.label == "Most common catalyst")
    # Pd(OAc)2 appears 4 times of 8, the mode
    assert cat_card.value == "Pd(OAc)2"


def test_worst_yield_card_appears_when_below_50(df):
    cards = build_summary_cards(df)
    labels = {c.label for c in cards}
    assert "Worst yield" in labels


def test_no_worst_yield_card_when_no_outlier():
    """Build a small df without a yield below 50 — worst card should NOT appear."""
    rows = [
        {"id": "x", "title": "ok", "yield_pct": 80.0, "catalyst": "Pd(OAc)2", "solvent": "toluene"}
        for _ in range(5)
    ]
    df = pd.DataFrame(rows)
    cards = build_summary_cards(df)
    labels = {c.label for c in cards}
    assert "Worst yield" not in labels
