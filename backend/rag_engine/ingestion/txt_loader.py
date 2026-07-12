from pathlib import Path
from backend.rag_engine.models.document import Document


class TextLoader:
    """
    Loader responnsible for reading plain text (.txt) files.
    """

    def load(self, file_path: str) -> list[Document]:
        """
        Read a text file and return a Document object.
        """
        path = Path(file_path)

        text = path.read_text(encoding="utf-8", errors="ignore")

        return [
            Document(
                content=text,
                source=path.name,
                file_type="txt",
                metadata={"size": path.stat().st_size},
            )
        ]
