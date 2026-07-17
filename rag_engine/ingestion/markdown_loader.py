from pathlib import Path
from rag_engine.models.document import Document
from rag_engine.ingestion.base_loader import BaseLoader
from core.logger import logger


class MarkdownLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        path = self.validate(file_path)

        logger.info(f"Loading Markdown Content: {path.name}")
        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            documents = [
                Document(
                    content=text,
                    source=path.name,
                    file_type="md",
                    metadata={
                        "file_size": path.stat().st_size,
                    },
                )
            ]

        except Exception:
            logger.exception(f"Failed loading Markdown: {path.name}")
            raise
        
        logger.info(f"Loaded Markdown: {path.name}")
        return documents
