"""AnalysisResult — chart-ready data returned by AnalyzeService.

Shape is intentionally flexible: every chart_type uses a different subset of fields.
The frontend renderer (Task #12) keys off `chart_data.chart_type` and reads the relevant
fields. Keeps the API single-shaped (one /ask response type) without forcing a 6-way
discriminated union.
"""
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from faraday_engine.domain.query_spec import ChartType


class SummaryCard(BaseModel):
    """One of the 3 cards next to the chart — count, average, mode, etc."""
    label: str                       # "Matched experiments"
    value: str                       # "12"
    sublabel: str | None = None      # "of 210 total"


class ChartPoint(BaseModel):
    """Generic point — covers scatter (x,y[,color]), bar (x=category, y=value),
    timeseries (x=date, y=value, series=category)."""
    x: str | float | datetime
    y: float | None = None
    color: str | None = None         # group_by category for scatter coloring
    series: str | None = None        # group_by category for timeseries
    count: int | None = None         # samples behind an aggregated point
    id: str | None = None            # experiment id for click-through


class HeatmapCell(BaseModel):
    """One cell in a 2-D heatmap (group_by × group_by_secondary)."""
    x: str                           # group_by category
    y: str                           # group_by_secondary category
    value: float | None              # aggregated metric value
    count: int                       # samples in this cell


class HistogramBin(BaseModel):
    bin_low: float
    bin_high: float
    count: int


class MatchedExperiment(BaseModel):
    """Compact representation for the matched list shown beside the chart."""
    id: str
    title: str
    type: str
    status: str
    yield_pct: float | None
    started_at: datetime | None
    catalyst: str | None = None
    solvent: str | None = None


class ChartData(BaseModel):
    """Chart-shape-flexible: each chart_type populates the fields it needs."""
    model_config = ConfigDict(use_enum_values=True)

    chart_type: ChartType
    x_label: str = ""
    y_label: str = ""

    points: list[ChartPoint] = Field(default_factory=list)
    heatmap_cells: list[HeatmapCell] = Field(default_factory=list)
    histogram_bins: list[HistogramBin] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """What AnalyzeService.analyze returns. Drives the entire Ask-mode UI render."""
    chart_data: ChartData
    summary_cards: list[SummaryCard] = Field(default_factory=list)
    matched_experiments: list[MatchedExperiment] = Field(default_factory=list)
    total_matched: int = 0
    intent: str = ""                 # echoed from QuerySpec for the UI heading
