from pathlib import Path
from docx import Document as DocxDocument
from backend.rag_engine.models.document import Document
from backend.rag_engine.ingestion.base_loader import BaseLoader


class DocxLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        path = self.validate(file_path)

        doc = DocxDocument(path)

        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        content = "\n".join(paragraphs)

        return [
            Document(
                content=content,
                source=path.name,
                file_type="docx",
                metadata={
                    "paragraphs": len(paragraphs),
                    "file_size": path.stat().st_size,
                },
            )
        ]
