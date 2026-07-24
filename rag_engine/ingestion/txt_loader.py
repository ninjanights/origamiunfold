from rag_engine.models.document import Document
from rag_engine.ingestion.base_loader import BaseLoader
from core.logger import logger


class TextLoader(BaseLoader):

    def load(self, file_path: str, progress=None) -> list[Document]:

        if progress:
            progress.upload(
                "loading_txt",
                "Reading TXT",
                20,
                preview="File 2. 'abc abc   def  #'",
                after="File 2. 'abc abc   def  #'",
            )

        path = self.validate(file_path)
        file_size = path.stat().st_size

        logger.info(f"Loading Text: {path.name}")
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")

            documents = [
                Document(
                    content=text,
                    source=path.name,
                    file_type="txt",
                    metadata={"file_size": file_size},
                )
            ]
        except Exception:
            logger.exception(f"Failed loading Text: {path.name}")
            raise
        if progress:
            loaded_preview = text[:80] if text else "File 2. 'abc abc   def  #'"
            progress.upload(
                "txt_loaded",
                f"Loaded {len(documents)} page.",
                25,
                preview=loaded_preview,
                after=loaded_preview,
            )

        logger.info(f"Loaded Text: {path.name}")
        return documents
