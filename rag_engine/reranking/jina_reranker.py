import requests

from core.settings import settings

from rag_engine.models.chunk import Chunk
from rag_engine.reranking.base_reranker import BaseReranker
from backend.realtime.progress_reporter import ProgressReporter


class JinaReranker(BaseReranker):

    URL = "https://api.jina.ai/v1/rerank"

    def rerank(
        self,
        query: str,
        chunks: list[Chunk],
        top_k: int,
        progress: ProgressReporter | None = None,
    ) -> list[Chunk]:
        chunks_prev = f"Found {len(chunks)} passages."
        if progress:
            progress.chat(
                "reranker_started",
                f"Reranking {len(chunks)} retrieved passages...",
                52,
                preview=chunks_prev,
                after=f"Reranking {len(chunks)} passages...",
            )

        if not chunks:
            return []

        payload = {
            "model": settings.RERANKER_MODEL,
            "query": query,
            "documents": [chunk.content for chunk in chunks],
            "top_n": top_k,
            "return_documents": False,
        }

        headers = {
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        if progress:
            progress.chat(
                "reranker_processing",
                "Jina is evaluating relevance...",
                54,
                preview=f"Reranking {len(chunks)} passages...",
                after="Evaluating relevance...",
            )

        response = requests.post(
            self.URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        results = response.json()["results"]

        reranked_preview = f"Selected top {top_k} passages."
        if progress:
            progress.chat(
                "reranker_finished",
                f"Selected top {top_k} passages.",
                56,
                preview="Evaluating relevance...",
                after=reranked_preview,
            )

        reranked_chunks = [chunks[item["index"]] for item in results]

        return reranked_chunks
