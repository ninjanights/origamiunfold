import requests

from core.settings import settings

from rag_engine.models.chunk import Chunk
from rag_engine.reranking.base_reranker import BaseReranker


class JinaReranker(BaseReranker):

    URL = "https://api.jina.ai/v1/rerank"

    def rerank(
        self,
        query: str,
        chunks: list[Chunk],
        top_k: int,
    ) -> list[Chunk]:

        if not chunks:
            return []

        payload = {
            "model": settings.RERANKER_MODEL,
            "query": query,
            "documents": [
                chunk.content
                for chunk in chunks
            ],
            "top_n": top_k,
            "return_documents": False,
        }

        headers = {
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        results = response.json()["results"]

        reranked_chunks = [
            chunks[item["index"]]
            for item in results
        ]

        return reranked_chunks