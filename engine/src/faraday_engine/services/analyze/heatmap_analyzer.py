"""Heatmap — group_by × group_by_secondary cells, value = aggregated metric."""
import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.analysis_result import HeatmapCell
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer


@AnalyzerRegistry.register(ChartType.HEATMAP)
class HeatmapAnalyzer(ChartAnalyzer):
    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData:
        if spec.group_by == GroupBy.NONE.value or spec.group_by_secondary == GroupBy.NONE.value:
            return ChartData(chart_type=ChartType.HEATMAP)

        metric = spec.metric
        agg = self._pandas_agg(spec.aggregation)
        x_col, y_col = spec.group_by, spec.group_by_secondary
        valid = df if agg == "count" else df.dropna(subset=[metric])

        if valid.empty:
            return ChartData(
                chart_type=ChartType.HEATMAP,
                x_label=x_col.replace("_", " ").title(),
                y_label=y_col.replace("_", " ").title(),
            )

        grouped = (
            valid.groupby([x_col, y_col], dropna=False)[metric]
            .agg([agg, "count"])
            .reset_index()
            .rename(columns={agg: "value"})
        )

        cells = [
            HeatmapCell(
                x=str(row[x_col]) if pd.notna(row[x_col]) else "(unknown)",
                y=str(row[y_col]) if pd.notna(row[y_col]) else "(unknown)",
                value=float(row["value"]) if pd.notna(row["value"]) else None,
                count=int(row["count"]),
            )
            for _, row in grouped.iterrows()
        ]

        return ChartData(
            chart_type=ChartType.HEATMAP,
            x_label=x_col.replace("_", " ").title(),
            y_label=y_col.replace("_", " ").title(),
            heatmap_cells=cells,
        )
