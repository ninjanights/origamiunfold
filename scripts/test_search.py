from backend.rag_engine.embeddings.bge_embedder import BGEEmbedder
from backend.rag_engine.vectorstore.chroma_store import ChromaStore

embedder = BGEEmbedder()
store = ChromaStore()

embedding = embedder.embed_text("what is python?")

results = store.search(embedding, top_k=3)


for chunk in results:
    print("=" * 80)
    print(f"ID           : {chunk.id}")
    print(f"Source       : {chunk.source}")
    print(f"File Type    : {chunk.file_type}")
    print(f"Page Number  : {chunk.page_number}")
    print(f"Chunk Number : {chunk.chunk_number}")
    print(f"Metadata     : {chunk.metadata}")
    print("\nContent:\n")
    print(chunk.content)
    print()