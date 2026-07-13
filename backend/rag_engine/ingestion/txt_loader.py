from pathlib import Path
from backend.rag_engine.models.document import Document
from backend.rag_engine.ingestion.base_loader import BaseLoader


class TextLoader(BaseLoader):

    def load(self, file_path: str) -> list[Document]:
        path = self.validate(file_path)

        text = path.read_text(encoding="utf-8", errors="ignore")

        return [
            Document(
                content=text,
                source=path.name,
                file_type="txt",
                metadata={"size": path.stat().st_size},
            )
        ]
