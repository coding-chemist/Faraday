"""Tests for engine/services/analyze/dataframe.py."""
from faraday_engine.services.analyze.dataframe import experiments_to_dataframe


def test_empty_experiments_returns_empty_dataframe():
    df = experiments_to_dataframe([])
    assert df.empty
    # All canonical columns are present even when empty
    assert {"id", "title", "yield_pct", "catalyst", "solvent", "month"}.issubset(df.columns)


def test_denormalizes_catalyst_and_base(df):
    assert "catalyst" in df.columns
    assert "base" in df.columns
    assert df["catalyst"].notna().all()
    assert (df["base"] == "potassium carbonate").all()


def test_month_column_is_yyyy_mm_format(df):
    months = df["month"].dropna()
    assert all(len(m) == 7 and m[4] == "-" for m in months)


def test_yield_pct_is_none_when_no_result(df):
    # exp 8 has no result
    null_yields = df[df["yield_pct"].isna()]
    assert len(null_yields) == 1
    assert null_yields.iloc[0]["title"] == "exp 8"
