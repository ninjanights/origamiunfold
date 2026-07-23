from pathlib import Path
from rag_engine.models.document import Document
from rag_engine.ingestion.base_loader import BaseLoader
from core.logger import logger


class PdfLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:


        # lazy
        import fitz
        path = self.validate(file_path)
        file_size = path.stat().st_size
        documents: list[Document] = []

        logger.info(f"Loading PDF: {path.name}")

        try:
            with fitz.open(path) as pdf:
                total_pages = len(pdf)
                for page_index, page in enumerate(pdf):
                    text = page.get_text("text")
                    if not text.strip():
                        continue

                    documents.append(
                        Document(
                            content=text,
                            source=path.name,
                            file_type="pdf",
                            page_number=page_index + 1,
                            metadata={
                                "page": page_index + 1,
                                "total_pages": total_pages,
                                "file_size": file_size,
                            },
                        )
                    )
        except Exception:
            logger.exception(f"Failed loading PDF: {path.name}")
            raise

        logger.info(f"Loaded {len(documents)} pages from {path.name}")
        return documents
