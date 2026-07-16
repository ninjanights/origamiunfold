from backend.core.logger import logger

from backend.rag_engine.chunking.base_chunker import BaseChunker
from backend.rag_engine.embeddings.base_embedder import BaseEmbedder
from backend.rag_engine.ingestion.loader import DocumentLoader
from backend.rag_engine.preprocessing.pipeline import PreprocessingPipeline
from backend.rag_engine.vectorstore.base_vectorstore import BaseVectorStore


class IndexingService:
    def __init__(
        self,
        loader: DocumentLoader,
        pipeline: PreprocessingPipeline,
        chunker: BaseChunker,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore,
    ):
        self.loader = loader
        self.pipeline = pipeline
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

    def index(self, file_path: str) -> None:
        logger.info(f"Indexing document: {file_path}")
        try:
            documents = self.loader.load(file_path)
            documents = [self.pipeline.process(document) for document in documents]

            chunks = []

            for doc in documents:
                chunks.extend(self.chunker.chunk(doc))

            logger.info(f"Created {len(chunks)} chunks.")

            for chunk in chunks:
                chunk.embedding = self.embedder.embed_text(chunk.content)

            logger.info("Embeddings generated.")
            self.vector_store.add(chunks)

            logger.info(f"Indexed {len(chunks)} chunks successfully.")
        except Exception:
            logger.exception(f"Failed to index document: {file_path}")
            raise
