from rag_engine.models.chunk import Chunk
from backend.realtime.progress_reporter import ProgressReporter


class PromptBuilder:
    def build(
        self,
        question: str,
        chunks: list[Chunk],
        progress: ProgressReporter | None = None,
    ) -> str:
        chunks_prev = f"Selected {len(chunks)} passages." if chunks else "No passages."
        if progress:
            progress.chat(
                "building_prompt",
                "Building AI prompt...",
                60,
                preview=chunks_prev,
                after="Building AI prompt...",
            )
        context = "\n\n".join(chunk.content for chunk in chunks)
        if progress:
            progress.chat(
                "prompt_ready",
                f"Prepared {len(chunks)} context passages.",
                65,
                preview="Building AI prompt...",
                after=f"Prepared {len(chunks)} context passages.",
            )

        prompt = f"""
        You are a helpful AI assistant.
        Answer ONLY from the provided context.
        If the answer is not present in the context, say:
        "I couldn't find that information in the provided documents."

        Context
        {context}.
        Question
        {question}.
        Answer:
        """
        return prompt.strip()
