from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "jina-embeddings-v3"
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 30))
    SESSION_CLEANUP_INTERVAL = int(os.getenv("SESSION_CLEANUP_INTERVAL", 30))
