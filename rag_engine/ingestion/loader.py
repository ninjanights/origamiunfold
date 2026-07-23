from pathlib import Path

from rag_engine.ingestion.txt_loader import TextLoader
from rag_engine.ingestion.pdf_loader import PdfLoader
from rag_engine.ingestion.docx_loader import DocxLoader
from rag_engine.ingestion.csv_loader import CsvLoader
from rag_engine.ingestion.excel_loader import ExcelLoader
from rag_engine.ingestion.json_loader import JsonLoader
from rag_engine.ingestion.markdown_loader import MarkdownLoader




class DocumentLoader:
    def load(self, file_path: str):
        extension = Path(file_path).suffix.lower()

        if extension == ".txt":
            loader = TextLoader()

        elif extension == ".pdf":
            loader = PdfLoader()

        elif extension == ".docx":
            loader = DocxLoader()

        elif extension == ".csv":
            loader = CsvLoader()

        elif extension in (".xlsx", ".xls"):
            loader = ExcelLoader()

        elif extension == ".json":
            loader = JsonLoader()

        elif extension == ".md":
            loader = MarkdownLoader()

        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load(file_path)