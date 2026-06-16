"""Scatter — raw points, x=date, y=metric, color=group_by category."""
import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.analysis_result import ChartPoint
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer


@AnalyzerRegistry.register(ChartType.SCATTER)
class ScatterAnalyzer(ChartAnalyzer):
    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData:
        metric = spec.metric
        valid = df.dropna(subset=[metric, "started_at"])
        color_col = None if spec.group_by == GroupBy.NONE.value else spec.group_by

        points = [
            ChartPoint(
                x=row["started_at"],
                y=float(row[metric]),
                color=str(row[color_col]) if color_col and pd.notna(row[color_col]) else None,
                id=row["id"],
            )
            for _, row in valid.iterrows()
        ]

        return ChartData(
            chart_type=ChartType.SCATTER,
            x_label="Date",
            y_label=metric.replace("_", " ").title(),
            points=points,
        )
