"""QueryParserService — converts NL queries to validated QuerySpec via the LLM provider.

The prompt is auto-generated from the QuerySpec enums — adding a new enum value
(chart_type, group_by, aggregation, metric) automatically appears in the prompt.
No prompt edit needed.

instructor + Pydantic handle JSON shape + retries inside the provider; we only ship
the prompt + service.
"""
from datetime import datetime
from datetime import timedelta

from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType
from faraday_engine.domain.query_spec import Aggregation
from faraday_engine.domain.query_spec import ChartType
from faraday_engine.domain.query_spec import GroupBy
from faraday_engine.domain.query_spec import Metric
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.providers.llm.base import LLMProvider
from faraday_shared.logging import get_logger

log = get_logger(__name__)


_SYSTEM_PROMPT = """\
You are a query-understanding service for an electronic lab notebook used by industry chemists.

Convert the chemist's natural-language question into a QuerySpec JSON object.

Today is {today_iso}. Resolve any relative dates (e.g. "last 6 months", "this year") to
absolute ISO datetimes using this reference.

ENUMS (use exact values):
  reaction_type:         {types}
  status:                {statuses}
  chart_type:            {charts}
  group_by:              {groups}
  group_by_secondary:    {groups}     (only used for heatmap; otherwise leave as "none")
  aggregation:           {aggs}
  metric:                {metrics}

GUIDELINES
- Leave filter fields null when the user didn't constrain them.
- "yield below X" => yield_max=X. "yield above X" => yield_min=X.
- "compare A vs B by X" => group_by=X, chart_type=bar.
- "trend over time" / "by month" => chart_type=timeseries, group_by=month.
- "show me" / "list" with no metric implies chart_type=list.
- "distribution of yields" => chart_type=histogram, metric=yield_pct.
- "X by Y across Z" or "X by Y AND Z" => chart_type=heatmap, group_by=Y, group_by_secondary=Z.
- "intent" is a one-sentence restatement of what you understood, written for the chemist.

EXAMPLES

User: "Show Suzuki couplings where yield was below 70% in the last six months, colored by catalyst"
Output:
{{
  "reaction_type": "suzuki_coupling",
  "yield_max": 70,
  "date_from": "{six_months_ago_iso}",
  "chart_type": "scatter",
  "group_by": "catalyst",
  "aggregation": "count",
  "metric": "yield_pct",
  "intent": "Suzuki couplings with yield below 70% in the last 6 months, grouped by catalyst"
}}

User: "Compare HATU vs EDC amide coupling yields"
Output:
{{
  "reaction_type": "amide_coupling",
  "chart_type": "bar",
  "group_by": "catalyst",
  "aggregation": "mean",
  "metric": "yield_pct",
  "intent": "Average amide coupling yields compared across coupling reagents"
}}

User: "Average yield by reaction type this year"
Output:
{{
  "date_from": "{year_start_iso}",
  "chart_type": "bar",
  "group_by": "reaction_type",
  "aggregation": "mean",
  "metric": "yield_pct",
  "intent": "Average yield grouped by reaction type for the current year"
}}

User: "Yield by catalyst across solvents"
Output:
{{
  "chart_type": "heatmap",
  "group_by": "catalyst",
  "group_by_secondary": "solvent",
  "aggregation": "mean",
  "metric": "yield_pct",
  "intent": "Average yield as a heatmap of catalyst × solvent"
}}

Now convert this query:
User: "{user_query}"
Output:
"""


def _build_prompt(user_query: str, today: datetime) -> str:
    six_months_ago = today - timedelta(days=180)
    year_start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    return _SYSTEM_PROMPT.format(
        today_iso=today.date().isoformat(),
        six_months_ago_iso=six_months_ago.isoformat(),
        year_start_iso=year_start.isoformat(),
        types=", ".join(t.value for t in ExperimentType),
        statuses=", ".join(s.value for s in ExperimentStatus),
        charts=", ".join(c.value for c in ChartType),
        groups=", ".join(g.value for g in GroupBy),
        aggs=", ".join(a.value for a in Aggregation),
        metrics=", ".join(m.value for m in Metric),
        user_query=user_query,
    )


class QueryParserService:
    """Verb: parse. NL string in, validated QuerySpec out."""

    def __init__(self, llm: LLMProvider, today: datetime | None = None) -> None:
        self._llm = llm
        self._today = today  # None => resolve at call time so tests can fix it

    def parse(self, nl_query: str) -> QuerySpec:
        today = self._today or datetime.utcnow()
        prompt = _build_prompt(nl_query, today)
        log.info("query.parse.start", query=nl_query, query_chars=len(nl_query))
        spec = self._llm.parse(prompt, response_model=QuerySpec)
        log.info(
            "query.parse.done",
            chart_type=spec.chart_type,
            group_by=spec.group_by,
            group_by_secondary=spec.group_by_secondary,
            reaction_type=spec.reaction_type,
            intent=spec.intent,
        )
        return spec
