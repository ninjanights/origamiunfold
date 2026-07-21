from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    print("BASE_DIR:", BASE_DIR)
    print("API KEY:", os.getenv("GEMINI_API_KEY"))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-base-en-v1.5",
    )
    RERANKER_MODEL = os.getenv(
        "RERANKER_MODEL",
        "BAAI/bge-reranker-base",
    )

    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        "./backend/chroma_db",
    )

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", 1000)
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", 200)
    )

    TOP_K = int(
        os.getenv("TOP_K", 5)
    )

    TEMPERATURE = float(
        os.getenv("TEMPERATURE", 0.2)
    )

    MAX_TOKENS = int(
        os.getenv("MAX_TOKENS", 2048)
    )
    
    
    GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite"
)


settings = Settings()