from backend.rag_engine.embeddings.base_embedder import BaseEmbedder
from backend.rag_engine.models.chunk import Chunk
from backend.rag_engine.vectorstore.base_vectorstore import BaseVectorStore
from backend.rag_engine.retriever.filters import SearchFilters


class Retriever:
    def __init__(
        self,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore,
    ):
        self.embedder = embedder
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int = 3,
        filters: SearchFilters | None = None,
    ) -> list[Chunk]:

        if not query.strip():
            raise ValueError("Query cannot be empty.")
        embedding = self.embedder.embed_text(query)

        return self.vector_store.search(
            embedding=embedding, top_k=top_k, filters=filters
        )
