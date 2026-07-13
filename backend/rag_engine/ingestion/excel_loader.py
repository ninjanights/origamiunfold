from pathlib import Path
import pandas as pd
from backend.rag_engine.models.document import Document


class ExcelLoader:
    def load(self, file_path: str) -> list[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

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
                    },
                )
            )
        return documents
