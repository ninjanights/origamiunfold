from backend.rag_engine.llm.base_llm import BaseLLM


class LLMItself(BaseLLM):

    def __init__(self):
        pass

    def generate(
        self,
        prompt: str,
    ) -> str:

        raise NotImplementedError