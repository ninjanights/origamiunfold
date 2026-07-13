from uuid import uuid4

from backend.rag_engine.embeddings.bge_embedder import BGEEmbedder
from backend.rag_engine.models.chunk import Chunk
from backend.rag_engine.vectorstore.chroma_store import ChromaStore

embedder = BGEEmbedder()
store = ChromaStore()

chunk = Chunk(
    id=str(uuid4()),
    content="Python is an amazing programming language.",
    source="sample.txt",
    file_type="txt",
)

chunk.embedding = embedder.embed_text(chunk.content)

store.add([chunk])

print("Inserted successfully!")