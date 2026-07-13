from abc import ABC, abstractmethod

from backend.core.logger import logger
from backend.rag_engine.models.document import Document
from backend.rag_engine.models.chunk import Chunk


class BaseChunker(ABC):
    def validate(self, document: Document) -> Document:
        if not isinstance(document, Document):
            raise TypeError("Expected a Document instance.")
        if not document.content.strip():
            raise ValueError("Document content is empty.")

        logger.info(f"Chunking document: {document.source}")
        return document

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]: ...
