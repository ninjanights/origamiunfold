from pathlib import Path

from backend.rag_engine.ingestion.txt_loader import TextLoader
from backend.rag_engine.ingestion.pdf_loader import PdfLoader

class DocumentLoader:
    """
    Main entry point for loading supported documents.
    Chooses the correct loader based on file extension.
    """

    def __init__(self):
        self.loaders = {
            ".txt": TextLoader(),
            ".pdf": PdfLoader()
        }
    
    def load(self, file_path: str):
        path = Path(file_path)

        extension = path.suffix.lower()
        loader = self.loaders.get(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")
        
        return loader.load(file_path)