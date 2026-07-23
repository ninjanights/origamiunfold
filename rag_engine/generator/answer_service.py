from sessions.session_model import SessionModel
from core.model_registry import ModelRegistry
from services.retrieval_service import RetrievalService
from rag_engine.prompts.prompt_builder import PromptBuilder
import time


class AnswerService:

    @property
    def retriever(self):
        if not hasattr(self, "_retriever"):
            self._retriever = RetrievalService()
        return self._retriever

    @property
    def prompt_builder(self):
        if not hasattr(self, "_prompt_builder"):
            self._prompt_builder = PromptBuilder()
        return self._prompt_builder

    @property
    def llm(self):
        if not hasattr(self, "_llm"):
            self._llm = ModelRegistry.llm_model()
        return self._llm

    def answer(
        self,
        question: str,
        session: SessionModel,
        sources: list[str] | None = None,
    ) -> dict:
        chunks = self.retriever.retrieve(
            question=question, session=session, sources=sources
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
