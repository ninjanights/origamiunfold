from sessions.session_model import SessionModel
from core.model_registry import ModelRegistry
from services.retrieval_service import RetrievalService
from rag_engine.prompts.prompt_builder import PromptBuilder
import time
from backend.realtime.progress_reporter import ProgressReporter


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
        progress: ProgressReporter | None = None,
    ) -> dict:
        if progress:
            progress.chat(
                "retrieving_context",
                "Searching relevant documents...",
                15,
                preview=f"Question: {question}",
                after="Searching relevant documents...",
            )
        chunks = self.retriever.retrieve(
            question=question, session=session, sources=sources, progress=progress
        )
        prompt = self.prompt_builder.build(
            question=question, chunks=chunks, progress=progress
        )
        for i in range(3):
            try:
                response = self.llm.generate(prompt, progress=progress)
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

        if progress:
            ans_prev = f"Answer is {response[:60]}" if response else "Answer ready."
            progress.chat(
                "completed",
                "Answer ready.",
                100,
                preview=ans_prev,
                after="The answer we found",
            )
        return {"answer": response, "sources": sources}
