from pathlib import Path
import pandas as pd
from backend.rag_engine.models.document import Document
from backend.rag_engine.ingestion.base_loader import BaseLoader


class CsvLoader(BaseLoader):
    def load(self, file_path: str) -> list[Document]:
        path = self.validate(file_path)

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
                    },
                )
            )

        return documents
