from backend.core.logger import logger

from backend.rag_engine.llm.base_llm import BaseLLM
from backend.rag_engine.prompts.prompt_builder import PromptBuilder
from backend.rag_engine.services.retrieval_service import RetrievalService


class RAGService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_builder: PromptBuilder,
        llm: BaseLLM,
    ):
        self.retrieval_service = retrieval_service
        self.prompt_builder = prompt_builder
        self.llm = llm

    def ask(
        self,
        question: str,
    ) -> str:
        logger.info("Retrieving relevant chunks...")
        chunks = self.retrieval_service.retrieve(question)
        logger.info("Building prompt...")

        prompt = self.prompt_builder.build(
            question,
            chunks,
        )
        logger.info("Generating answer...")
        answer = self.llm.generate(prompt)
        return answer