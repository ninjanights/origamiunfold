from abc import ABC, abstractmethod
from pathlib import Path
from backend.rag_engine.models.document import Document


class BaseLoader(ABC):
    def validate(self, file_path: str) -> Path:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        if not path.is_file():
            raise ValueError(f"{path} is not a file.")

        return path

    @abstractmethod
    def load(self, file_path: str) -> list[Document]: ...
