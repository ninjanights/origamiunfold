from google import genai
from core.settings import settings
from rag_engine.llm.base_llm import BaseLLM


class LLMItself(BaseLLM):

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate(
        self,
        prompt: str,
    ) -> str:
        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            return response.text
        except Exception:
            raise
