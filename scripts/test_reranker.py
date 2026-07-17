from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.reranking.bge_reranker import BGEReranker
from rag_engine.retriever.retriever import Retriever
from rag_engine.vectorstore.chroma_store import ChromaStore

embedder = BGEEmbedder()
store = ChromaStore()
retriever = Retriever(embedder, store)

reranker = BGEReranker()

chunks = retriever.search(
    "What is Python?",
    top_k=10,
)

results = reranker.rerank(
    query="What is Python?",
    chunks=chunks,
    top_k=3,
)

for chunk in results:
    print("=" * 80)
    print(chunk.score)
    print(chunk.content)
