from backend.core.logger import logger

from backend.rag_engine.embeddings.base_embedder import BaseEmbedder
from backend.rag_engine.retriever.retriever import Retriever
from backend.rag_engine.reranking.base_reranker import BaseReranker
from backend.rag_engine.models.chunk import Chunk


class RetrievalService:

    def __init__(
        self,
        embedder: BaseEmbedder,
        retriever: Retriever,
        reranker: BaseReranker,
    ):
        self.embedder = embedder
        self.retriever = retriever
        self.reranker = reranker

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> list[Chunk]:
        logger.info(f"Searching: {question}")
        embedding = self.embedder.embed_text(question)
        chunks = self.retriever.retrieve(
            embedding=embedding,
            top_k=top_k,
        )
        chunks = self.reranker.rerank(
            question,
            chunks,
        )
        return chunks
