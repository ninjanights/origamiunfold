from rag_engine.ingestion.loader import DocumentLoader

from rag_engine.preprocessing.pipeline import PreprocessingPipeline

from rag_engine.chunking.recursive_chunker import RecursiveChunker

from rag_engine.embeddings.bge_embedder import BGEEmbedder

from rag_engine.vectorstore.chroma_store import ChromaStore

from rag_engine.retriever.retriever import Retriever

from rag_engine.reranking.bge_reranker import BGEReranker

from rag_engine.prompts.prompt_builder import PromptBuilder

from rag_engine.llm.llm_itself import LLMItself

from rag_engine.services.indexing_service import IndexingService

from rag_engine.services.retrieval_service import RetrievalService

from rag_engine.services.rag_service import RAGService


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