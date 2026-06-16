"""Bar — x = group_by category, y = aggregated metric."""
import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.analysis_result import ChartPoint
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer


@AnalyzerRegistry.register(ChartType.BAR)
class BarAnalyzer(ChartAnalyzer):
    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData:
        metric = spec.metric
        agg = self._pandas_agg(spec.aggregation)
        group = spec.group_by if spec.group_by != GroupBy.NONE.value else None

        if df.empty:
            return ChartData(chart_type=ChartType.BAR, x_label=group or "Total", y_label=metric)

        if group is None:
            value = float(df[metric].agg(agg)) if agg != "count" else float(df[metric].count())
            point = ChartPoint(x="all", y=value, count=int(df[metric].count()))
            return ChartData(
                chart_type=ChartType.BAR,
                x_label="Total",
                y_label=f"{agg.title()} {metric.replace('_', ' ')}",
                points=[point],
            )

        valid = df if agg == "count" else df.dropna(subset=[metric])
        grouped = (
            valid.groupby(group, dropna=False)[metric]
            .agg([agg, "count"])
            .reset_index()
            .rename(columns={agg: "value"})
            .sort_values("value", ascending=False)
        )

        points = [
            ChartPoint(
                x=str(row[group]) if pd.notna(row[group]) else "(unknown)",
                y=float(row["value"]) if pd.notna(row["value"]) else None,
                count=int(row["count"]),
            )
            for _, row in grouped.iterrows()
        ]

        return ChartData(
            chart_type=ChartType.BAR,
            x_label=group.replace("_", " ").title(),
            y_label=f"{agg.title()} {metric.replace('_', ' ')}",
            points=points,
        )
