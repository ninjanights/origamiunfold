from sessions.session_model import SessionModel

from rag_engine.vectorstore.chroma_store import ChromaStore
from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.retriever.filters import SearchFilters
from core.settings import settings
from core.logger import logger
from rag_engine.embeddings.jina_embedder import JinaEmbedder
from rag_engine.reranking.jina_reranker import JinaReranker


class RetrievalService:

    @property
    def embedder(self):
        if not hasattr(self, "_embedder"):

            if settings.EMBEDDING_PROVIDER == "jina":
                self._embedder = JinaEmbedder()

            else:
                self._embedder = BGEEmbedder()

        return self._embedder

    @property
    def vector_store(self):
        if not hasattr(self, "_vector_store"):
            self._vector_store = ChromaStore()
        return self._vector_store

    @property
    def reranker(self):
        if not settings.ENABLE_RERANKER:
            return None

        if not hasattr(self, "_reranker"):
            self._reranker = JinaReranker()

        return self._reranker

    def retrieve(
        self,
        question: str,
        session: SessionModel,
        top_k: int = 3,
        sources: list[str] | None = None,
    ):
        query_embedding = self.embedder.embed_text(question)

        chunks = self.vector_store.search(
            embedding=query_embedding,
            filters=SearchFilters(
                session_id=session.session_id,
                sources=sources,
            ),
            top_k=settings.TOP_K,
        )
        if not settings.ENABLE_RERANKER:
            logger.info("Reranker disabled.")

        if self.reranker:
            chunks = self.reranker.rerank(
                query=question,
                chunks=chunks,
                top_k=top_k,
            )
        return chunks
