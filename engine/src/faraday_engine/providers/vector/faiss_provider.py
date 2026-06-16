"""FAISS vector store. IndexFlatIP (inner-product) with id mapping persisted to disk."""
import json
from pathlib import Path

import faiss
import numpy as np

from faraday_engine.providers.llm.base import ProviderConfig
from faraday_engine.providers.vector.base import ScoredId, VectorProvider, VectorRegistry
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class FAISSConfig(ProviderConfig):
    index_path: str = "./data/faiss_index"
    dim: int = 768  # nomic-embed-text default; override per embed model


@VectorRegistry.register("faiss", config=FAISSConfig)
class FAISSProvider(VectorProvider):
    def __init__(self, config: FAISSConfig) -> None:
        super().__init__(config)
        self._config: FAISSConfig = config
        self._dir = Path(config.index_path)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._index_file = self._dir / "index.faiss"
        self._ids_file = self._dir / "ids.json"
        self._index: faiss.Index | None = None
        self._ids: list[str] = []
        self._loaded_mtime: float = 0.0
        self.load()

    def _reload_if_stale(self) -> None:
        """If the on-disk index is newer than what we loaded (another process wrote),
        reload. Lets API + worker share a FAISS file without a separate vector server."""
        if not self._index_file.exists():
            return
        current_mtime = self._index_file.stat().st_mtime
        if current_mtime > self._loaded_mtime:
            self.load()

    def _ensure_index(self) -> faiss.Index:
        if self._index is None:
            self._index = faiss.IndexFlatIP(self._config.dim)
        return self._index

    def upsert(self, id: str, vector: list[float]) -> None:
        self.upsert_batch([(id, vector)])

    def upsert_batch(self, items: list[tuple[str, list[float]]]) -> None:
        if not items:
            return
        index = self._ensure_index()
        # Remove any pre-existing ids by rebuilding (FAISS IndexFlatIP doesn't support delete-by-id)
        new_ids = {id for id, _ in items}
        if any(id in self._ids for id in new_ids):
            keep = [(i, id) for i, id in enumerate(self._ids) if id not in new_ids]
            if keep:
                keep_vecs = index.reconstruct_n(0, index.ntotal)
                keep_vecs = np.stack([keep_vecs[i] for i, _ in keep])
                self._index = faiss.IndexFlatIP(self._config.dim)
                self._index.add(keep_vecs)
                self._ids = [id for _, id in keep]
            else:
                self._index = faiss.IndexFlatIP(self._config.dim)
                self._ids = []
            index = self._index

        vecs = np.asarray([v for _, v in items], dtype=np.float32)
        # Normalize for cosine sim via inner product
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        vecs = vecs / np.clip(norms, a_min=1e-12, a_max=None)
        index.add(vecs)
        self._ids.extend(id for id, _ in items)
        log.debug("faiss.upsert", count=len(items), total=len(self._ids))

    def search(self, vector: list[float], k: int = 20) -> list[ScoredId]:
        self._reload_if_stale()
        if self._index is None or self._index.ntotal == 0:
            return []
        q = np.asarray([vector], dtype=np.float32)
        q = q / np.clip(np.linalg.norm(q, axis=1, keepdims=True), a_min=1e-12, a_max=None)
        scores, idxs = self._index.search(q, min(k, self._index.ntotal))
        return [
            ScoredId(id=self._ids[i], score=float(s))
            for s, i in zip(scores[0], idxs[0], strict=True)
            if i != -1
        ]

    def delete(self, id: str) -> None:
        if id not in self._ids:
            return
        # Rebuild without the deleted id (FAISS Flat doesn't support delete-by-id natively)
        keep = [(i, _id) for i, _id in enumerate(self._ids) if _id != id]
        if not keep:
            self._index = faiss.IndexFlatIP(self._config.dim)
            self._ids = []
            return
        assert self._index is not None
        old_vecs = self._index.reconstruct_n(0, self._index.ntotal)
        keep_vecs = np.stack([old_vecs[i] for i, _ in keep])
        self._index = faiss.IndexFlatIP(self._config.dim)
        self._index.add(keep_vecs)
        self._ids = [id for _, id in keep]

    def persist(self) -> None:
        if self._index is None:
            return
        faiss.write_index(self._index, str(self._index_file))
        self._ids_file.write_text(json.dumps(self._ids))
        self._loaded_mtime = self._index_file.stat().st_mtime
        log.info("faiss.persist", path=str(self._index_file), count=len(self._ids))

    def load(self) -> None:
        if self._index_file.exists() and self._ids_file.exists():
            self._index = faiss.read_index(str(self._index_file))
            self._ids = json.loads(self._ids_file.read_text())
            self._loaded_mtime = self._index_file.stat().st_mtime
            log.info("faiss.load", path=str(self._index_file), count=len(self._ids))
