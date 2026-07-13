from pathlib import Path
from backend.rag_engine.models.document import Document


class MarkdownLoader:
    def load(self, file_path: str) -> list[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return [
            Document(
                content=text,
                source=path.name,
                file_type="md",
                metadata={
                    "file_size": path.stat().st_size,
                },
            )
        ]
