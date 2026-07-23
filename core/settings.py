from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        "./storage/chroma",
    )

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K = int(os.getenv("TOP_K", 5))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2048))
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))
    
    
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "jina-embeddings-v3",
    )
    # Reranker (Jina only)
    ENABLE_RERANKER = os.getenv(
        "ENABLE_RERANKER",
        "true",
    ).lower() == "true"


    RERANKER_MODEL = "jina-reranker-v2-base-multilingual"
    RERANKER_MODEL = os.getenv(
        "RERANKER_MODEL",
        "jina-reranker-v2-base-multilingual",
    )

    JINA_API_KEY = os.getenv("JINA_API_KEY")


settings = Settings()
