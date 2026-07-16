from backend.rag_engine.ingestion.loader import DocumentLoader

from backend.rag_engine.preprocessing.pipeline import PreprocessingPipeline

from backend.rag_engine.chunking.recursive_chunker import RecursiveChunker

from backend.rag_engine.embeddings.bge_embedder import BGEEmbedder

from backend.rag_engine.vectorstore.chroma_store import ChromaStore

from backend.rag_engine.retriever.retriever import Retriever

from backend.rag_engine.reranking.bge_reranker import BGEReranker

from backend.rag_engine.prompts.prompt_builder import PromptBuilder

from backend.rag_engine.llm.llm_itself import LLMItself

from backend.rag_engine.services.indexing_service import IndexingService

from backend.rag_engine.services.retrieval_service import RetrievalService

from backend.rag_engine.services.rag_service import RAGService


loader = DocumentLoader()

pipeline = PreprocessingPipeline()

chunker = RecursiveChunker()

embedder = BGEEmbedder()

vector_store = ChromaStore()

retriever = Retriever(vector_store)

reranker = BGEReranker()

prompt_builder = PromptBuilder()

llm = LLMItself()


retrieval_service = RetrievalService(
    embedder=embedder,
    retriever=retriever,
    reranker=reranker,
)

indexing_service = IndexingService(
    loader=loader,
    pipeline=pipeline,
    chunker=chunker,
    embedder=embedder,
    vector_store=vector_store,
)

rag_service = RAGService(
    retrieval_service=retrieval_service,
    prompt_builder=prompt_builder,
    llm=llm,
)