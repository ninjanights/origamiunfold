from pathlib import Path
from rag_engine.models.document import Document
from rag_engine.ingestion.base_loader import BaseLoader
from core.logger import logger


class CsvLoader(BaseLoader):
    def load(self, file_path: str, progress=None) -> list[Document]:
        
        if progress:
            progress.upload(
        "loading_csv",
        "Reading CSV",
        20,
    )
        
        # lazy
        import pandas as pd
        path = self.validate(file_path)
        file_size = path.stat().st_size
        logger.info(f"Loading CSV: {path.name}")
        try:
            df = pd.read_csv(path)
            documents = []

            for index, row in df.iterrows():
                text = "\n".join(f"{column}: {value}" for column, value in row.items())

                documents.append(
                    Document(
                        content=text,
                        source=path.name,
                        file_type="csv",
                        metadata={
                            "row": index,
                            "columns": list(df.columns),
                            "file_size": file_size,
                        },
                    )
                )
        except Exception:
            logger.exception(f"Failed loading CSV: {path.name}")
            raise
        if progress:
            progress.upload(
        "csv_loaded",
        f"Loaded {len(documents)} page(s).",
        25,
    )

        logger.info(f"Loaded {len(documents)} pages from {path.name}")
        return documents
