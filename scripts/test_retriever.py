from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.retriever.retriever import Retriever
from rag_engine.vectorstore.chroma_store import ChromaStore
from rag_engine.retriever.filters import SearchFilters

embedder = BGEEmbedder()
store = ChromaStore()

retriever = Retriever(embedder, store)

results = retriever.search(
    "Python",
    top_k=3,
    filters=SearchFilters(file_type="txt")
)

print(f"\nRetrieved {len(results)} chunk(s)\n")

for chunk in results:
    print("=" * 80)
    print(chunk.content)
    print(chunk.score)
