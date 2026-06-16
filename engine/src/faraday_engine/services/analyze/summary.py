"""Summary cards — the three small panels next to the chart.

Cards are deterministic given a DataFrame: count, avg yield, most-common catalyst.
A 4th outlier card appears when there's a clear worst-yield experiment.
"""
import pandas as pd

from faraday_engine.domain.analysis_result import SummaryCard


def build_summary_cards(df: pd.DataFrame, total_in_db: int | None = None) -> list[SummaryCard]:
    """Return 3-4 SummaryCard entries based on what's in the DataFrame.

    Empty df → just "0 matched" card. Helps surface 'no results' without a special UI path.
    """
    if df.empty:
        return [SummaryCard(label="Matched experiments", value="0")]

    cards: list[SummaryCard] = []

    matched = len(df)
    sub = f"of {total_in_db} total" if total_in_db else None
    cards.append(SummaryCard(label="Matched experiments", value=str(matched), sublabel=sub))

    yields = df["yield_pct"].dropna()
    if not yields.empty:
        cards.append(SummaryCard(
            label="Average yield",
            value=f"{yields.mean():.1f}%",
            sublabel=f"median {yields.median():.1f}%",
        ))

    catalysts = df["catalyst"].dropna()
    if not catalysts.empty:
        mode_catalyst = catalysts.mode().iloc[0]
        share = (catalysts == mode_catalyst).mean() * 100
        cards.append(SummaryCard(
            label="Most common catalyst",
            value=str(mode_catalyst),
            sublabel=f"{share:.0f}% of runs",
        ))

    if not yields.empty and yields.min() < 50 and matched >= 5:
        worst_idx = yields.idxmin()
        worst_title = df.loc[worst_idx, "title"]
        cards.append(SummaryCard(
            label="Worst yield",
            value=f"{yields.min():.1f}%",
            sublabel=_truncate(worst_title, 60),
        ))

    return cards


def _truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"
