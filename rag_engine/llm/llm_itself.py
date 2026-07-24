from google import genai
from core.settings import settings
from rag_engine.llm.base_llm import BaseLLM
from backend.realtime.progress_reporter import ProgressReporter


class LLMItself(BaseLLM):

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate(
        self,
        prompt: str,
        progress: ProgressReporter | None = None,
    ) -> str:
        if progress:
            progress.chat(
                "connecting_llm",
                "Connecting to Gemini",
                70,
                preview="Prepared context passages.",
                after="Connecting to Gemini...",
            )
        try:
            if progress:
                progress.chat(
                    "generating_answer",
                    "Generating answer...",
                    80,
                    preview="Connecting to Gemini...",
                    after="Generating answer...",
                )
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            if progress:
                ans_prev = f"Answer preview is {response.text[:60]}" if response and response.text else "Answer generated successfully."
                progress.chat(
                    "answer_generated",
                    "Answer generated successfully.",
                    95,
                    preview="Generating answer...",
                    after=ans_prev,
                )

            return response.text
        except Exception:
            if progress:
                progress.chat(
                    "generation_failed",
                    "Failed to generate answer.",
                    95,
                    preview="Generating answer...",
                    after="Generation failed.",
                )
            raise
