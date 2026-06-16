"""POST /ask — Lab Memory Ask mode orchestration.

Wires four engine pieces end-to-end:
    NL query
       -> QueryParserService.parse        (LLM)
    QuerySpec
       -> spec.to_filters()
    ExperimentFilters
       -> ExperimentService.list           (SQL)
    list[Experiment]
       -> AnalyzeService.analyze           (pandas)
    AnalysisResult
       -> HTTP response (this file)

Route stays thin — orchestration only. Each step's logic lives in its own service.
"""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from faraday_api.deps import get_analyze_service
from faraday_api.deps import get_experiment_service
from faraday_api.deps import get_query_parser_service
from faraday_api.schemas.ask import AskRequest
from faraday_engine.domain.analysis_result import AnalysisResult
from faraday_engine.services.analyze_service import AnalyzeService
from faraday_engine.services.experiment_service import ExperimentService
from faraday_engine.services.query_parser_service import QueryParserService
from faraday_shared.logging import get_logger

log = get_logger(__name__)

router = APIRouter(tags=["ask"])


@router.post("/ask", response_model=AnalysisResult)
def ask(
    request: AskRequest,
    parser: QueryParserService = Depends(get_query_parser_service),
    experiments: ExperimentService = Depends(get_experiment_service),
    analyzer: AnalyzeService = Depends(get_analyze_service),
) -> AnalysisResult:
    log.info("ask.start", query=request.query)

    try:
        spec = parser.parse(request.query)
    except Exception as exc:
        log.exception("ask.parse_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not understand the query: {exc}",
        ) from exc

    filters = spec.to_filters()
    matched = experiments.list(filters)
    total = experiments.count_total()
    result = analyzer.analyze(spec, matched, total_in_db=total)

    log.info(
        "ask.done",
        intent=result.intent,
        chart_type=result.chart_data.chart_type,
        matched=result.total_matched,
    )
    return result
