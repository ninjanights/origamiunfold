from sentence_transformers import CrossEncoder

from core.logger import logger
from rag_engine.models.chunk import Chunk
from rag_engine.reranking.base_reranker import BaseReranker


class BGEReranker(BaseReranker):
    _model = None

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):
        if BGEReranker._model is None:
            logger.info(f"Loading reranker: {model_name}")

            BGEReranker._model = CrossEncoder(model_name)
        self.model = BGEReranker._model

    # rerank fn

    def rerank(self, query: str, chunks: list[Chunk], top_k: int) -> list[Chunk]:
        if not chunks:
            return []

        pairs = [(query, chunk.content) for chunk in chunks]

        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk.score = float(score)

        chunks.sort(
            key=lambda chunk: chunk.score,
            reverse=True,
        )

        return chunks[:top_k]
