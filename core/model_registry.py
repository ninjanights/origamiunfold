from sentence_transformers import SentenceTransformer
from rag_engine.llm.llm_itself import LLMItself


class ModelRegistry:
    _embedding_model = None
    _llm_model = None

    @classmethod
    def embedding_model(cls):
        if cls._embedding_model is None:
            cls._embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

        return cls._embedding_model

    @classmethod
    def llm_model(cls):
        if cls._llm_model is None:
            cls._llm_model = LLMItself()

        return cls._llm_model
