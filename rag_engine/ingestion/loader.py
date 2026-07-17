from pathlib import Path

from rag_engine.ingestion.txt_loader import TextLoader
from rag_engine.ingestion.pdf_loader import PdfLoader
from rag_engine.ingestion.docx_loader import DocxLoader
from rag_engine.ingestion.csv_loader import CsvLoader
from rag_engine.ingestion.excel_loader import ExcelLoader
from rag_engine.ingestion.json_loader import JsonLoader
from rag_engine.ingestion.markdown_loader import MarkdownLoader


class DocumentLoader:
    """
    Main entry point for loading supported documents.
    Chooses the correct loader based on file extension.
    """

    def __init__(self):
        self.loaders = {
            ".txt": TextLoader(),
            ".pdf": PdfLoader(),
            ".docx": DocxLoader(),
            ".csv": CsvLoader(),
            ".xlsx": ExcelLoader(),
            ".xls": ExcelLoader(),
            ".json": JsonLoader(),
            ".md": MarkdownLoader(),
        }

    def load(self, file_path: str):
        path = Path(file_path)

        extension = path.suffix.lower()
        loader = self.loaders.get(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load(file_path)
