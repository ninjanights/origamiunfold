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
    def __init__(self):
        self.loader = DocumentLoader()
        self.cleaner = Cleaner()
        self.normalizer = Normalizer()
        self.duplicate_remover = Deduplicator()
        self.chunker = RecursiveChunker()
        self.embedder = BGEEmbedder()
        self.vector_store = ChromaStore()

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
