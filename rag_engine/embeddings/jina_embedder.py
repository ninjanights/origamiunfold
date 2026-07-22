from core.settings import settings
from rag_engine.embeddings.base_embedder import BaseEmbedder
from rag_engine.models.chunk import Chunk
import requests


class JinaEmbedder(BaseEmbedder):

    URL = "https://api.jina.ai/v1/embeddings"

    def embed_text(
        self,
        text: str,
    ) -> list[float]:

        response = requests.post(
            self.URL,
            headers={
                "Authorization": f"Bearer {settings.JINA_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.EMBEDDING_MODEL,
                "input": [text],
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

    def embed_chunks(
        self,
        chunks: list[Chunk],
    ) -> list[list[float]]:

        texts = [chunk.content for chunk in chunks]

        response = requests.post(
            self.URL,
            headers={
                "Authorization": f"Bearer {settings.JINA_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.EMBEDDING_MODEL,
                "input": texts,
            },
            timeout=30,
        )

        response.raise_for_status()

        return [item["embedding"] for item in response.json()["data"]]
