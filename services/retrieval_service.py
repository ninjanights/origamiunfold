from sessions.session_model import SessionModel

from rag_engine.vectorstore.chroma_store import ChromaStore
from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.retriever.filters import SearchFilters


class RetrievalService:

    @property
    def embedder(self):
        if not hasattr(self, "_embedder"):
            self._embedder = BGEEmbedder()
        return self._embedder

    @property
    def vector_store(self):
        if not hasattr(self, "_vector_store"):
            self._vector_store = ChromaStore()
        return self._vector_store

    def retrieve(
        self,
        question: str,
        session: SessionModel,
        top_k: int = 3,
        sources: list[str] | None = None,
    ):
        query_embedding = self.embedder.embed_text(question)

        return self.vector_store.search(
            embedding=query_embedding,
            filters=SearchFilters(
                session_id=session.session_id,
                sources=sources,
            ),
            top_k=top_k,
        )
