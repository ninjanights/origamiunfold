from pathlib import Path
import fitz
from backend.rag_engine.models.document import Document


class PdfLoader:
    """
    Loads PDF documents and returns one Document object per page.

    Responsibilities:
    - Open PDF
    - Extract text
    - Preserve page numbers
    - Attach metadata
    """

    def load(self, file_path: str) -> list[Document]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        documents: list[Document] = []

        pdf = fitz.open(path)

        try:
            total_pages = len(pdf)
            for page_index, page in enumerate(pdf):
                text = page.get_text("text")
                if not text.strip():
                    continue

                document = Document(
                    content=text,
                    source=path.name,
                    file_type="pdf",
                    page_number=page_index + 1,
                    metadata={
                        "page": page_index + 1,
                        "total_pages": total_pages,
                        "file_size": path.stat().st_size,
                    },
                )

                documents.append(document)

        finally:
            pdf.close()

        return documents
