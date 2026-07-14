from backend.rag_engine.embeddings.base_embedder import BaseEmbedder
from backend.rag_engine.models.chunk import Chunk
from backend.rag_engine.vectorstore.base_vectorstore import BaseVectorStore


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
    ) -> list[Chunk]:
        embedding = self.embedder.embed_text(query)

        return self.vector_store.search(embedding=embedding, top_k=top_k)
