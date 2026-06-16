"""Timeseries — aggregated metric over time buckets (month), series = group_by category."""
import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.analysis_result import ChartPoint
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer


@AnalyzerRegistry.register(ChartType.TIMESERIES)
class TimeseriesAnalyzer(ChartAnalyzer):
    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData:
        metric = spec.metric
        agg = self._pandas_agg(spec.aggregation)
        valid = df.dropna(subset=["month"])
        if metric != "count" and agg != "count":
            valid = valid.dropna(subset=[metric])

        series_col = None if spec.group_by == GroupBy.NONE.value else spec.group_by
        group_cols = ["month"] + ([series_col] if series_col else [])

        if valid.empty:
            return ChartData(chart_type=ChartType.TIMESERIES, x_label="Month", y_label=metric)

        grouped = (
            valid.groupby(group_cols, dropna=False)[metric]
            .agg([agg, "count"])
            .reset_index()
            .rename(columns={agg: "value"})
        )

        points = [
            ChartPoint(
                x=str(row["month"]),
                y=float(row["value"]) if pd.notna(row["value"]) else None,
                series=str(row[series_col]) if series_col and pd.notna(row[series_col]) else None,
                count=int(row["count"]),
            )
            for _, row in grouped.iterrows()
        ]
        points.sort(key=lambda p: (p.x, p.series or ""))

        return ChartData(
            chart_type=ChartType.TIMESERIES,
            x_label="Month",
            y_label=f"{agg.title()} {metric.replace('_', ' ')}",
            points=points,
        )
