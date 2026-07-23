from pathlib import Path

from rag_engine.ingestion.loader import DocumentLoader
from rag_engine.preprocessing.cleaner import Cleaner
from rag_engine.preprocessing.normalizer import Normalizer
from rag_engine.preprocessing.deduplicator import Deduplicator
from rag_engine.chunking.recursive_chunker import RecursiveChunker
from rag_engine.vectorstore.chroma_store import ChromaStore

from rag_engine.embeddings.jina_embedder import JinaEmbedder

from core.settings import settings
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
            self._embedder = JinaEmbedder()

        return self._embedder

    @property
    def vector_store(self):
        if not hasattr(self, "_vector_store"):
            self._vector_store = ChromaStore()
        return self._vector_store

    # --------------------------------------------------------

    def index(self, file_path: Path, session: SessionModel) -> None:

        documents = self.loader.load(file_path)
        all_chunks = []
        for doc in documents:

            doc.content = self.cleaner.clean(doc.content)
            doc.content = self.normalizer.normalize(doc.content)
            doc.content = self.duplicate_remover.remove_duplicates(doc.content)
            chunks = self.chunker.chunk(doc)

            for chunk in chunks:
                chunk.session_id = session.session_id
            all_chunks.extend(chunks)

        embeddings = self.embedder.embed_chunks(all_chunks)
        for chunk, embedding in zip(all_chunks, embeddings):
            chunk.embedding = embedding

        self.vector_store.add(all_chunks)
        logger.info(f"Chunks created: {len(all_chunks)}")
