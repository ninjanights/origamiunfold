from abc import ABC, abstractmethod
from rag_engine.models.chunk import Chunk
from rag_engine.retriever.filters import SearchFilters


class BaseVectorStore:
    @abstractmethod
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = 3,
        filters: SearchFilters | None = None,
    ) -> list[Chunk]: ...
    @abstractmethod
    def delete(
        self,
        ids: list[str],
    ) -> None: ...
    @abstractmethod
    def clear(self) -> None: ...
