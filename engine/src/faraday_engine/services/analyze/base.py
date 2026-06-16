"""Chart analyzer base + registry.

Same decorator pattern as LLM/Vector providers, FilterRules, FitRules. One declarative
entry per chart_type; AnalyzeService stays generic.
"""
from abc import ABC
from abc import abstractmethod
from typing import ClassVar

import pandas as pd

from faraday_engine.domain.analysis_result import ChartData
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import QuerySpec


_AGG_FUNCS: dict[str, str] = {
    "count": "count",
    "mean": "mean",
    "median": "median",
    "min": "min",
    "max": "max",
}


class ChartAnalyzer(ABC):
    """One analyzer per chart_type. Takes a prepared DataFrame + the spec; returns ChartData."""

    chart_type: ClassVar[ChartType]

    @abstractmethod
    def analyze(self, df: pd.DataFrame, spec: QuerySpec) -> ChartData: ...

    @staticmethod
    def _pandas_agg(aggregation: str) -> str:
        return _AGG_FUNCS.get(aggregation, "count")


class AnalyzerRegistry:
    """chart_type → analyzer class. Populated at import time by decorators."""

    _analyzers: ClassVar[dict[ChartType, type[ChartAnalyzer]]] = {}

    @classmethod
    def register(cls, chart_type: ChartType):
        def wrap(analyzer_cls: type[ChartAnalyzer]) -> type[ChartAnalyzer]:
            if chart_type in cls._analyzers:
                raise ValueError(f"Analyzer for {chart_type} already registered")
            analyzer_cls.chart_type = chart_type
            cls._analyzers[chart_type] = analyzer_cls
            return analyzer_cls
        return wrap

    @classmethod
    def resolve(cls, chart_type: str) -> ChartAnalyzer:
        # `chart_type` arrives as a string (use_enum_values=True on QuerySpec)
        for ct, analyzer_cls in cls._analyzers.items():
            if ct.value == chart_type:
                return analyzer_cls()
        raise ValueError(
            f"No analyzer for chart_type '{chart_type}'. "
            f"Registered: {sorted(ct.value for ct in cls._analyzers)}"
        )

    @classmethod
    def list(cls) -> list[str]:
        return sorted(ct.value for ct in cls._analyzers.keys())
