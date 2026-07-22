from rag_engine.ingestion.loader import DocumentLoader

from rag_engine.preprocessing.pipeline import PreprocessingPipeline

from rag_engine.chunking.recursive_chunker import RecursiveChunker

from rag_engine.embeddings.bge_embedder import BGEEmbedder

from rag_engine.vectorstore.chroma_store import ChromaStore

from rag_engine.retriever.retriever import Retriever

from rag_engine.reranking.bge_reranker import BGEReranker

from rag_engine.prompts.prompt_builder import PromptBuilder

from rag_engine.llm.llm_itself import LLMItself

from services.indexing_service import IndexingService

from services.retrieval_service import RetrievalService


loader = DocumentLoader()

pipeline = PreprocessingPipeline()

chunker = RecursiveChunker()

embedder = BGEEmbedder()

vector_store = ChromaStore()

retriever = Retriever(vector_store)

reranker = BGEReranker()

prompt_builder = PromptBuilder()

llm = LLMItself()


def get_indexing_service():
    return IndexingService(
        loader=loader,
        pipeline=pipeline,
        chunker=chunker,
        embedder=BGEEmbedder(),
        vector_store=ChromaStore(),
    )

def get_retrieval_service():
    return RetrievalService(
        embedder=BGEEmbedder(),
        retriever=Retriever(ChromaStore()),
        reranker=BGEReranker(),
    )
