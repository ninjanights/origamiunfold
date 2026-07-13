from chromadb import PersistentClient
import json
from backend.core.logger import logger
from backend.rag_engine.models.chunk import Chunk
from backend.rag_engine.vectorstore.base_vectorstore import BaseVectorStore


class ChromaStore(BaseVectorStore):
    def __init__(
        self,
        persist_directory: str = "./storage/chroma",
        collection_name: str = "origamidocuments",
    ):
        self.client = PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logger.info(f"Connected to Chroma collection: {collection_name}")

    def _serialize_metadata(self, chunk: Chunk) -> dict:
        metadata = {
            "source": chunk.source,
            "file_type": chunk.file_type,
            "page_number": chunk.page_number or 0,
            "chunk_number": chunk.chunk_number,
        }

        for key, value in chunk.metadata.items():
            if value is None:
                continue
            if isinstance(value, (str, int, float, bool)):

                metadata[key] = value
            else:
                metadata[key] = json.dumps(value)
        return metadata

    def add(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        self.collection.add(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.content for chunk in chunks],
            embeddings=[chunk.embedding for chunk in chunks],
            metadatas=[self._serialize_metadata(chunk) for chunk in chunks],
        )
        logger.info(f"Inserted {len(chunks)} chunks.")

    def search(self, embedding: list[float], top_k: int = 3):
        return self.collection.query(query_embeddings=[embedding], n_results=top_k)

    def delete(
        self,
        ids: list[str],
    ):
        self.collection.delete(ids=ids)

    def clear(self):

        self.client.delete_collection(self.collection.name)

        self.collection = self.client.get_or_create_collection(self.collection.name)

        logger.info("Collection cleared.")
