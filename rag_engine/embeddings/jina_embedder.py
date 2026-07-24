from core.settings import settings
from rag_engine.embeddings.base_embedder import BaseEmbedder
from rag_engine.models.chunk import Chunk
import requests
from backend.realtime.progress_reporter import ProgressReporter


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
        progress: ProgressReporter | None = None,
    ) -> list[list[float]]:
        chunks_preview = f"[{len(chunks)} chunks: '{chunks[0].content[:40]}']" if chunks else "abc cde efg"
        if progress:
            progress.upload(
                "embedding_start",
                f"Generating embeddings for {len(chunks)} chunks...",
                60,
                preview=chunks_preview,
                after="Generating embeddings...",
            )

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

        embeddings = [item["embedding"] for item in response.json()["data"]]
        if progress:
            emb_preview = f"[[{embeddings[0][0]:.2f}], [{embeddings[0][1]:.2f}], {embeddings[0][2]:.2f}]" if embeddings and len(embeddings[0]) >= 3 else "[[1.43], [7.18], 0.11]"
            progress.upload(
                "embedding_done",
                f"Generated {len(embeddings)} embeddings.",
                75,
                preview=chunks_preview,
                after=emb_preview,
            )
        return embeddings
