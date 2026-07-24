from sessions.session_model import SessionModel

from rag_engine.vectorstore.chroma_store import ChromaStore
from rag_engine.retriever.filters import SearchFilters
from core.settings import settings
from core.logger import logger
from rag_engine.embeddings.jina_embedder import JinaEmbedder
from rag_engine.reranking.jina_reranker import JinaReranker
from backend.realtime.progress_reporter import ProgressReporter


class RetrievalService:

    @property
    def embedder(self):
        if not hasattr(self, "_embedder"):
            self._embedder = JinaEmbedder()

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
        progress: ProgressReporter | None = None,
    ):
        q_preview = f"Query: {question}"
        if progress:
            progress.chat(
                "embedding_question",
                "Understanding your question...",
                20,
                preview=q_preview,
                after="Query Embedding example [[0.82], [3.14], 0.45]",
            )

        query_embedding = self.embedder.embed_text(question)
        if progress:
            progress.chat(
                "searching_documents",
                "Searching indexed documents...",
                35,
                preview="Query Embedding is [[0.82], [3.14], 0.45]",
                after="Searching indexed documents...",
            )
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

            if progress:
                progress.chat(
                    "reranking",
                    f"Ranking {len(chunks)} relevant passages...",
                    50,
                    preview=f"Found {len(chunks)} passages.",
                    after=f"Ranking {len(chunks)} passages...",
                )

            chunks = self.reranker.rerank(
                query=question,
                chunks=chunks,
                top_k=top_k,
                progress=progress,
            )

        passages_preview = (
            f"Selected {len(chunks)} passages: '{chunks[0].content[:40]}'"
            if chunks
            else "No passages."
        )
        if progress:
            progress.chat(
                "context_ready",
                f"Selected {len(chunks)} passages.",
                58,
                preview=passages_preview,
                after=passages_preview,
            )

        return chunks
