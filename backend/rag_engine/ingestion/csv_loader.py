from pathlib import Path
import pandas as pd
from backend.rag_engine.models.document import Document


class CsvLoader:
    def load(self, file_path: str) -> list[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

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
