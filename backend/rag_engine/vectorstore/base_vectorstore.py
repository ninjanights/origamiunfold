from abc import ABC, abstractmethod
from backend.rag_engine.models.chunk import Chunk


class BaseVectorStore:
    @abstractmethod
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = 3,
    ) -> list[Chunk]: ...
    @abstractmethod
    def delete(
        self,
        ids: list[str],
    ) -> None: ...
    @abstractmethod
    def clear(self) -> None: ...
