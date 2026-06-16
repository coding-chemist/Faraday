"""QuerySpec — structured representation of a user's NL question.

Produced by QueryParserService from the chemist's natural-language input. Drives the
rest of the Ask pipeline: filters become ExperimentFilters, group_by/aggregation/chart
drive the analyze and rendering stages.
"""
from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator

from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType


class ChartType(StrEnum):
    SCATTER = "scatter"          # continuous vs continuous (yield vs date)
    TIMESERIES = "timeseries"    # values over time
    BAR = "bar"                  # comparison across categories
    LIST = "list"                # no chart — matched experiments only
    HISTOGRAM = "histogram"      # distribution of a single metric


class Aggregation(StrEnum):
    COUNT = "count"
    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"


class GroupBy(StrEnum):
    CATALYST = "catalyst"
    SOLVENT = "solvent"
    BASE = "base"
    REACTION_TYPE = "reaction_type"
    MONTH = "month"
    NONE = "none"


Metric = Literal["yield_pct", "purity_pct", "temperature_c", "time_min"]


class QuerySpec(BaseModel):
    """The contract between NL parsing and downstream analyze/render stages.

    Flat by design — small enough that 7B local models can produce it reliably,
    expressive enough to cover the v0.1 Ask-mode query shapes.
    """
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    # --- Filter dimensions (mirror ExperimentFilters) ---
    reaction_type: ExperimentType | None = None
    status: ExperimentStatus | None = None
    catalyst_name: str | None = None
    solvent_name: str | None = None
    yield_min: float | None = Field(None, ge=0, le=100)
    yield_max: float | None = Field(None, ge=0, le=100)
    date_from: datetime | None = None
    date_to: datetime | None = None

    # --- Visualization + analysis ---
    chart_type: ChartType = ChartType.SCATTER
    group_by: GroupBy = GroupBy.NONE
    aggregation: Aggregation = Aggregation.COUNT
    metric: Metric = "yield_pct"

    # --- Echo back to chemist + useful for logs / debugging ---
    intent: str = Field(..., min_length=4, max_length=200)

    @model_validator(mode="after")
    def _yield_range_consistent(self) -> "QuerySpec":
        if self.yield_min is not None and self.yield_max is not None:
            if self.yield_min > self.yield_max:
                raise ValueError("yield_min cannot exceed yield_max")
        return self

    @model_validator(mode="after")
    def _date_range_consistent(self) -> "QuerySpec":
        if self.date_from is not None and self.date_to is not None:
            if self.date_from > self.date_to:
                raise ValueError("date_from cannot be after date_to")
        return self
