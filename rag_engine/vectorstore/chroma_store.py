from chromadb import PersistentClient
import json
from core.logger import logger
from rag_engine.models.chunk import Chunk
from rag_engine.vectorstore.base_vectorstore import BaseVectorStore
from rag_engine.retriever.filters import SearchFilters


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
            logger.warning("No chunks provided for insertion.")
            return
        if any(chunk.embedding is None for chunk in chunks):
            raise ValueError(
                "Every chunk must contain an embedding before being stored."
            )

        logger.info(f"Inserting {len(chunks)} chunks.")
        try:
            self.collection.add(
                ids=[chunk.id for chunk in chunks],
                documents=[chunk.content for chunk in chunks],
                embeddings=[chunk.embedding for chunk in chunks],
                metadatas=[self._serialize_metadata(chunk) for chunk in chunks],
            )
            logger.info(f"Inserted {len(chunks)} chunks.")
        except Exception:
            logger.exception("Failed to insert chunks into Chroma.")
            raise

    def _extract_metadata(self, metadata: dict) -> dict:
        reserved = {
            "source",
            "file_type",
            "page_number",
            "chunk_number",
        }
        return {key: value for key, value in metadata.items() if key not in reserved}

    def _deserialize_metadata(self, metadata: dict) -> dict:
        result = {}
        for key, value in metadata.items():
            if not isinstance(value, str):
                result[key] = value
                continue
            try:
                result[key] = json.loads(value)
            except Exception:
                result[key] = value
        return result

    # Convert filters to Chroma format - Private
    def _build_where(self, filters: SearchFilters | None) -> dict | None:
        if filters is None:
            return None
        where = {}
        if filters.source:
            where["source"] = filters.source
        if filters.file_type:
            where["file_type"] = filters.file_type
        if filters.page_number is not None:
            where["page_number"] = filters.page_number
        return where or None

    # search inside chroma
    def search(
        self,
        embedding: list[float],
        top_k: int = 3,
        filters: SearchFilters | None = None,
    ) -> list[Chunk]:

        if not embedding:
            raise ValueError("Search embedding cannot be empty.")

        logger.info(f"Searching top {top_k} chunks...")

        where = self._build_where(filters)
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        ids = result["ids"][0]

        chunks: list[Chunk] = []
        distances = result["distances"][0]

        for chunk_id, document, metadata, distance in zip(
            ids, documents, metadatas, distances
        ):
            metadata = self._deserialize_metadata(metadata)
            chunks.append(
                Chunk(
                    id=chunk_id,
                    content=document,
                    source=metadata.get("source", ""),
                    file_type=metadata.get("file_type", ""),
                    page_number=metadata.get("page_number"),
                    chunk_number=metadata.get("chunk_number", 0),
                    score=distance,
                    metadata=self._extract_metadata(metadata),
                )
            )
        logger.info(f"Retrieved {len(chunks)} chunks.")
        return chunks

    def delete(
        self,
        ids: list[str],
    ):
        self.collection.delete(ids=ids)

    def clear(self):

        self.client.delete_collection(self.collection.name)

        self.collection = self.client.get_or_create_collection(self.collection.name)

        logger.info("Collection cleared.")

    def show_all(self):
        return self.collection.get(
            include=[
                "documents",
                "metadatas",
                "embeddings",
            ]
        )
