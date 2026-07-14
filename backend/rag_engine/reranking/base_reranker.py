from abc import ABC, abstractmethod
from backend.rag_engine.models.chunk import Chunk


class BaseReranker(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: list[Chunk],
        top_k: int,
    ) -> list[Chunk]: ...
