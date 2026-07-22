from pathlib import Path

from rag_engine.ingestion.loader import DocumentLoader
from rag_engine.preprocessing.cleaner import Cleaner
from rag_engine.preprocessing.normalizer import Normalizer
from rag_engine.preprocessing.deduplicator import Deduplicator
from rag_engine.chunking.recursive_chunker import RecursiveChunker
from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.vectorstore.chroma_store import ChromaStore

from core.logger import logger

from sessions.session_model import SessionModel


class IndexingService:

    @property
    def loader(self):
        if not hasattr(self, "_loader"):
            self._loader = DocumentLoader()
        return self._loader

    @property
    def cleaner(self):
        if not hasattr(self, "_cleaner"):
            self._cleaner = Cleaner()
        return self._cleaner

    @property
    def normalizer(self):
        if not hasattr(self, "_normalizer"):
            self._normalizer = Normalizer()
        return self._normalizer

    @property
    def duplicate_remover(self):
        if not hasattr(self, "_duplicate_remover"):
            self._duplicate_remover = Deduplicator()
        return self._duplicate_remover

    @property
    def chunker(self):
        if not hasattr(self, "_chunker"):
            self._chunker = RecursiveChunker()
        return self._chunker

    @property
    def embedder(self):
        if not hasattr(self, "_embedder"):
            self._embedder = BGEEmbedder()
        return self._embedder

    @property
    def vector_store(self):
        if not hasattr(self, "_vector_store"):
            self._vector_store = ChromaStore()
        return self._vector_store
