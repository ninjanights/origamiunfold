from abc import ABC, abstractmethod
from rag_engine.models.chunk import Chunk


class BaseEmbedder(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> list[float]: ...

    @abstractmethod
    def embed_chunks(self, chunks: list[Chunk]) -> list[list[float]]: ...
