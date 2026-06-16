"""List — no chart data. AnalyzeService still populates matched_experiments separately."""
import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer


@AnalyzerRegistry.register(ChartType.LIST)
class ListAnalyzer(ChartAnalyzer):
    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData:
        # No chart — the matched_experiments list is what gets rendered.
        return ChartData(chart_type=ChartType.LIST)
