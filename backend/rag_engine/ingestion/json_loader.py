from pathlib import Path
import json
from backend.rag_engine.models.document import Document
from backend.rag_engine.ingestion.base_loader import BaseLoader


class JsonLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        path = self.validate(file_path)

        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        text = json.dumps(data, indent=2, ensure_ascii=False)

        return [
            Document(
                content=text,
                source=path.name,
                file_type="json",
                metadata={
                    "file_size": path.stat().st_size,
                },
            )
        ]
