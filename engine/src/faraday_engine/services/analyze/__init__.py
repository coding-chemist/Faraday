"""Analyzer subsystem — pluggable per chart_type.

Each analyzer registers itself on import. Adding a new chart type:
  1. Add `ChartType.X = "x"` to query_spec.py
  2. Drop a new x_analyzer.py here with @AnalyzerRegistry.register(ChartType.X)
  3. Add the import line below so the decorator runs

No edits to AnalyzeService.
"""
from faraday_engine.services.analyze.base import AnalyzerRegistry
from faraday_engine.services.analyze.base import ChartAnalyzer

# Importing each analyzer triggers @AnalyzerRegistry.register — keep imports greppable
from faraday_engine.services.analyze.bar_analyzer import BarAnalyzer  # noqa: F401
from faraday_engine.services.analyze.heatmap_analyzer import HeatmapAnalyzer  # noqa: F401
from faraday_engine.services.analyze.histogram_analyzer import HistogramAnalyzer  # noqa: F401
from faraday_engine.services.analyze.list_analyzer import ListAnalyzer  # noqa: F401
from faraday_engine.services.analyze.scatter_analyzer import ScatterAnalyzer  # noqa: F401
from faraday_engine.services.analyze.timeseries_analyzer import TimeseriesAnalyzer  # noqa: F401

__all__ = ["AnalyzerRegistry", "ChartAnalyzer"]
