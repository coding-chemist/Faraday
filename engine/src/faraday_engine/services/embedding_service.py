"""EmbeddingService — class.verb shape.

Generates embeddings via the LLM provider, persists in the vector provider. Same
service runs both as a Celery task (production: async on experiment create) and as
a direct call (seed/backfill scripts: synchronous batch).
"""
from collections.abc import Iterable

from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentFilters
from faraday_engine.providers.llm.base import LLMProvider
from faraday_engine.providers.vector.base import ScoredId
from faraday_engine.providers.vector.base import VectorProvider
from faraday_engine.repositories.experiment_repository import ExperimentRepository
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class EmbeddingService:
    """Verbs: create, search, delete, backfill."""

    def __init__(
        self,
        llm: LLMProvider,
        vector: VectorProvider,
        repository: ExperimentRepository,
    ) -> None:
        self._llm = llm
        self._vector = vector
        self._repository = repository

    def create(self, experiment_id: str, persist: bool = True) -> None:
        """Embed one experiment and upsert into the vector store.

        persist=False is for batch contexts (e.g. backfill) where we persist once at end.
        """
        experiment = self._repository.fetch(experiment_id)
        if experiment is None:
            raise KeyError(f"Experiment not found: {experiment_id}")
        text = experiment.to_searchable_text()
        vector = self._llm.embed(text)
        self._vector.upsert(experiment_id, vector)
        if persist:
            self._vector.persist()
        log.info("embedding.create", experiment_id=experiment_id, vector_len=len(vector))

    def search(self, query: str, k: int = 20) -> list[ScoredId]:
        """Embed the query, return top-k matching experiment IDs ranked by similarity."""
        vector = self._llm.embed(query)
        results = self._vector.search(vector, k)
        log.info("embedding.search", query_chars=len(query), k=k, hits=len(results))
        return results

    def delete(self, experiment_id: str) -> None:
        self._vector.delete(experiment_id)
        self._vector.persist()
        log.info("embedding.delete", experiment_id=experiment_id)

    def backfill(self, filters: ExperimentFilters | None = None, log_every: int = 25) -> int:
        """Re-embed every experiment that matches `filters`. Persists once at the end.

        Used after seed and after any change that affects the searchable text shape.
        Returns count embedded.
        """
        filters = filters or ExperimentFilters(limit=100_000)
        experiments: list[Experiment] = self._repository.list(filters)
        total = len(experiments)
        log.info("embedding.backfill.start", total=total)
        for i, experiment in enumerate(experiments, start=1):
            text = experiment.to_searchable_text()
            vector = self._llm.embed(text)
            self._vector.upsert(experiment.id, vector)
            if i % log_every == 0:
                log.info("embedding.backfill.progress", done=i, total=total)
        self._vector.persist()
        log.info("embedding.backfill.done", count=total)
        return total

    def embed_many(self, experiment_ids: Iterable[str]) -> int:
        """Embed an explicit list of experiment IDs (one-shot batch). Persists at end."""
        count = 0
        for experiment_id in experiment_ids:
            self.create(experiment_id, persist=False)
            count += 1
        self._vector.persist()
        return count
