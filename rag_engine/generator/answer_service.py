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
        session_id: SessionModel,
    ) -> str:
        chunks = self.retriever.retrieve(
            question=question,
            session=session_id,
        )
        prompt = self.prompt_builder.build(
            question=question,
            chunks=chunks,
        )

        response = self.llm.generate(prompt)

        sources = []
        for chunk in chunks:
            sources.append(
                {
                    "file": chunk.source,
                    "page": chunk.page_number,
                    "chunk": chunk.chunk_number,
                }
            )
        return {"answer": response, "sources": sources}
