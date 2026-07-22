from rag_engine.llm.llm_itself import LLMItself


class ModelRegistry:
    _llm_model = None

    @classmethod
    def llm_model(cls):
        if cls._llm_model is None:
            cls._llm_model = LLMItself()

        return cls._llm_model