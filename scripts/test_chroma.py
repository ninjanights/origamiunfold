from uuid import uuid4

from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.models.chunk import Chunk
from rag_engine.vectorstore.chroma_store import ChromaStore

embedder = BGEEmbedder()
store = ChromaStore()

chunk = Chunk(
    id=str(uuid4()),
    content="Python is an amazing programming language.",
    source="sample.txt",
    file_type="txt",
)

chunk.embedding = embedder.embed_text(chunk.content)

result = store.show_all()
print(result)
print("Inserted successfully!")