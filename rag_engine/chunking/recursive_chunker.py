from uuid import uuid4

from rag_engine.chunking.base_chunker import BaseChunker
from rag_engine.chunking.splitter import Splitter
from rag_engine.models.chunk import Chunk
from rag_engine.models.document import Document


class RecursiveChunker(BaseChunker):
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = Splitter()

    def chunk(self, document: Document) -> list[Chunk]:
        document = self.validate(document)
        chunks: list[Chunk] = []
        paragraphs = self.splitter.split_paragraphs(document.content)

        chunk_number = 1

        for paragraph in paragraphs:
            if len(paragraph) <= self.chunk_size:
                chunks.append(self._create_chunk(document, paragraph, chunk_number))
                chunk_number += 1
            else:
                sentences = self.splitter.split_sentences(paragraph)

                current = ""
                for sentence in sentences:
                    if len(current) + len(sentence) < self.chunk_size:
                        current += sentence + " "
                    else:
                        chunks.append(
                            self._create_chunk(document, current.strip(), chunk_number)
                        )

                        chunk_number += 1
                        
                        overlap = current[-self.chunk_overlap :]
                        
                        current = overlap + " " + sentence + " "
                if current:

                    chunks.append(
                        self._create_chunk(document, current.strip(), chunk_number)
                    )
                    chunk_number += 1

        return chunks

    def _create_chunk(
        self, document: Document, content: str, chunk_number: int
    ) -> Chunk:
        return Chunk(
            id=str(uuid4()),
            content=content,
            source=document.source,
            file_type=document.file_type,
            page_number=document.page_number,
            chunk_number=chunk_number,
            metadata=document.metadata.copy(),
        )
