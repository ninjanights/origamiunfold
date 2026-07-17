from pathlib import Path
import pandas as pd
from rag_engine.models.document import Document
from rag_engine.ingestion.base_loader import BaseLoader
from core.logger import logger


class ExcelLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        path = self.validate(file_path)
        file_size = path.stat().st_size

        logger.info(f"Loading Excel: {path.name}")
        try:
            workbook = pd.ExcelFile(path)
            documents = []

            for sheet in workbook.sheet_names:
                df = workbook.parse(sheet)
                text = df.to_string(index=False)

                documents.append(
                    Document(
                        content=text,
                        source=path.name,
                        file_type="xlsx",
                        metadata={
                            "sheet": sheet,
                            "rows": len(df),
                            "columns": list(df.columns),
                            "file_size": file_size,
                        },
                    )
                )
        except Exception:
            logger.exception(f"Failed loading Excel: {path.name}")
            raise

        return documents
