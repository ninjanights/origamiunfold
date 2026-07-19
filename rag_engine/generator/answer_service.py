from sessions.session_model import SessionModel
from core.model_registry import ModelRegistry
from services.retrieval_service import RetrievalService
from rag_engine.prompts.prompt_builder import PromptBuilder


class AnswerService:
    def __init__(self):
        self.retriever = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.llm = ModelRegistry.llm_model()
        
    def answer(
        self,
        question: str,
        session: SessionModel,
    ) -> str:
        chunks = self.retriever.retrieve(
            question=question,
            session=session,
        )
        prompt = self.prompt_builder.build(
            question=question,
            chunks=chunks,
        )

        response = self.llm.generate(prompt)

        return response