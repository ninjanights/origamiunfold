from sessions.session_model import SessionModel

from rag_engine.vectorstore.chroma_store import ChromaStore
from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.retriever.filters import SearchFilters


class RetrievalService:
    def __init__(self):
        self.embedder = BGEEmbedder()
        self.vector_store = ChromaStore()

    def retrieve(self, 
                 question: str, 
                 session: SessionModel, 
                 top_k: int = 3):
        query_embedding = self.embedder.embed_text(question)

        chunks = self.vector_store.search(
            embedding=query_embedding,
            filters=SearchFilters(
                session_id=session.session_id,
            ),
            top_k=top_k,

        )
        return chunks
