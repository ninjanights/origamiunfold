from abc import ABC, abstractmethod
from pathlib import Path
from rag_engine.models.document import Document
from core.logger import logger


class BaseLoader(ABC):
    def validate(self, file_path: str) -> Path:
        path = Path(file_path)

        if not path.exists():
            logger.error(f"File not found: {path}")
            raise FileNotFoundError(path)

        if not path.is_file():
            logger.error(f"{path} is not a file.")
            raise ValueError(f"{path} is not a file.")

        return path

    @abstractmethod
    def load(self, file_path: str) -> list[Document]: ...
