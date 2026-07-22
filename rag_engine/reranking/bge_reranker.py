from sentence_transformers import CrossEncoder

from core.logger import logger
from rag_engine.models.chunk import Chunk
from rag_engine.reranking.base_reranker import BaseReranker


class BGEReranker(BaseReranker):
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            logger.info("Loading BGE Reranker...")
            cls._model = CrossEncoder("BAAI/bge-reranker-base")

        return cls._model

    @property
    def model(self):
        return self.get_model()

    def rerank(self, query: str, chunks: list[Chunk], top_k: int) -> list[Chunk]:
        if not chunks:
            return []

        pairs = [(query, chunk.content) for chunk in chunks]

        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk.score = float(score)

        chunks.sort(
            key=lambda c: c.score,
            reverse=True,
        )

        return chunks[:top_k]