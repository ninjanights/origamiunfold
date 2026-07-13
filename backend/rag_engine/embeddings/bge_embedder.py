from backend.core.model_registry import ModelRegistry
from backend.rag_engine.embeddings.base_embedder import BaseEmbedder
from backend.rag_engine.models.chunk import Chunk


class BGEEmbedder(BaseEmbedder):

    def __init__(self):
        self.model = ModelRegistry.embedding_model()

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_chunks(
        self,
        chunks: list[Chunk],
    ) -> list[list[float]]:
        texts = [chunk.content for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )
        return embeddings.tolist()
