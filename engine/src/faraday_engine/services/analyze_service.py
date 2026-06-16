"""AnalyzeService — pure, no DB, no LLM.

Takes a QuerySpec + matched experiments, returns AnalysisResult. Dispatches to the
right ChartAnalyzer via AnalyzerRegistry. Adding a new chart_type doesn't touch this
file.
"""
from faraday_engine.domain.analysis_result import AnalysisResult
from faraday_engine.domain.analysis_result import MatchedExperiment
from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ReagentRole
from faraday_engine.domain.query_spec import QuerySpec
from faraday_engine.services.analyze import AnalyzerRegistry  # noqa: F401 — triggers registration
from faraday_engine.services.analyze.base import AnalyzerRegistry as Registry
from faraday_engine.services.analyze.dataframe import experiments_to_dataframe
from faraday_engine.services.analyze.summary import build_summary_cards
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class AnalyzeService:
    """Verb: analyze. QuerySpec + experiments in, AnalysisResult out."""

    def analyze(
        self,
        spec: QuerySpec,
        experiments: list[Experiment],
        total_in_db: int | None = None,
    ) -> AnalysisResult:
        df = experiments_to_dataframe(experiments)
        analyzer = Registry.resolve(spec.chart_type)
        chart_data = analyzer.analyze(df, spec)
        summary_cards = build_summary_cards(df, total_in_db=total_in_db)
        matched = [_to_matched(e) for e in experiments]

        log.info(
            "analyze.done",
            chart_type=spec.chart_type,
            matched=len(experiments),
            points=len(chart_data.points) + len(chart_data.heatmap_cells) + len(chart_data.histogram_bins),
        )

        return AnalysisResult(
            chart_data=chart_data,
            summary_cards=summary_cards,
            matched_experiments=matched,
            total_matched=len(experiments),
            intent=spec.intent,
        )


def _to_matched(exp: Experiment) -> MatchedExperiment:
    catalyst = next((r.name for r in exp.reagents if r.role == ReagentRole.CATALYST.value), None)
    return MatchedExperiment(
        id=exp.id,
        title=exp.title,
        type=exp.type,
        status=exp.status,
        yield_pct=exp.result.yield_pct if exp.result else None,
        started_at=exp.started_at,
        catalyst=catalyst,
        solvent=exp.solvent_name,
    )
