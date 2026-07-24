from pathlib import Path
from rag_engine.models.document import Document
from rag_engine.ingestion.base_loader import BaseLoader
from core.logger import logger


class JsonLoader(BaseLoader):
    def load(self, file_path: str, progress=None) -> list[Document]:
        if progress:
            progress.upload(
                "loading_json",
                "Reading JSON",
                20,
            )
        path = self.validate(file_path)

        # lazy
        import json

        logger.info(f"Loading JSON: {path.name}")
        try:

            with open(path, encoding="utf-8") as file:
                data = json.load(file)

                text = json.dumps(data, indent=2, ensure_ascii=False)

                documents = [
                    Document(
                        content=text,
                        source=path.name,
                        file_type="json",
                        metadata={
                            "file_size": path.stat().st_size,
                        },
                    )
                ]
        except Exception:
            logger.exception(f"Failed loading JSON: {path.name}")
            raise
        if progress:
            progress.upload(
                "json_loaded",
                f"Loaded {len(documents)} page.",
                25,
            )

        return documents
