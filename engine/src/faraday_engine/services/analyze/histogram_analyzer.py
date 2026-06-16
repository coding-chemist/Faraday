"""Histogram — distribution of a single metric."""
import numpy as np
import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.analysis_result import HistogramBin
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer


@AnalyzerRegistry.register(ChartType.HISTOGRAM)
class HistogramAnalyzer(ChartAnalyzer):
    """10 bins between observed min/max — sensible default that scales with the data."""

    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData:
        metric = spec.metric
        valid = df.dropna(subset=[metric])
        if valid.empty:
            return ChartData(
                chart_type=ChartType.HISTOGRAM,
                x_label=metric.replace("_", " ").title(),
                y_label="Count",
            )

        values = valid[metric].to_numpy()
        counts, edges = np.histogram(values, bins=10)
        bins = [
            HistogramBin(bin_low=float(edges[i]), bin_high=float(edges[i + 1]), count=int(counts[i]))
            for i in range(len(counts))
        ]

        return ChartData(
            chart_type=ChartType.HISTOGRAM,
            x_label=metric.replace("_", " ").title(),
            y_label="Count",
            histogram_bins=bins,
        )
