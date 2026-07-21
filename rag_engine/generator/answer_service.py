from sessions.session_model import SessionModel
from core.model_registry import ModelRegistry
from services.retrieval_service import RetrievalService
from rag_engine.prompts.prompt_builder import PromptBuilder
import time


class AnswerService:
    def __init__(self):
        self.retriever = RetrievalService()
        self.prompt_builder = PromptBuilder()
        self.llm = ModelRegistry.llm_model()

    def answer(
        self,
        question: str,
        session_id: SessionModel,
        sources: list[str] | None = None,
    ) -> str:
        chunks = self.retriever.retrieve(
            question=question, session=session_id, sources=sources
        )
        prompt = self.prompt_builder.build(
            question=question,
            chunks=chunks,
        )
        for i in range(3):
            try:
                response = self.llm.generate(prompt)
                break
            except Exception:
                if i == 2:
                    raise
                time.sleep(2)

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
