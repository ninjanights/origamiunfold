from sentence_transformers import SentenceTransformer


class ModelRegistry:
    _embedding_model = None

    @classmethod
    def embedding_model(cls):
        if cls._embedding_model is None:
            cls._embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

        return cls._embedding_model
