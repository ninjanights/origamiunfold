from pathlib import Path
import json
from backend.rag_engine.models.document import Document


class JsonLoader:
    def load(self, file_path: str) -> list[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

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
