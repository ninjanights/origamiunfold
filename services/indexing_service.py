from pathlib import Path

from rag_engine.ingestion.loader import DocumentLoader
from rag_engine.preprocessing.cleaner import Cleaner
from rag_engine.preprocessing.normalizer import Normalizer
from rag_engine.preprocessing.deduplicator import Deduplicator
from rag_engine.chunking.recursive_chunker import RecursiveChunker
from core.logger import logger

from sessions.session_model import SessionModel


class IndexingService:
    def __init__(self):
        self.loader = DocumentLoader()
        self.cleaner = Cleaner()
        self.normalizer = Normalizer()
        self.duplicate_remover = Deduplicator()
        self.chunker = RecursiveChunker()

    def index(self, file_path: Path, session: SessionModel) -> None:
        document = self.loader.load(file_path)
        document.content = self.cleaner.clean(document.content)

        document.content = self.normalizer.normalize(document.content)
        document.content = self.duplicate_remover.remove_duplicates(document.content)
        chunks = self.chunker.chunk(document)
        
        logger.info(f"Chunks created: {len(chunks)}")