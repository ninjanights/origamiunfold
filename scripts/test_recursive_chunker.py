from backend.rag_engine.chunking.recursive_chunker import RecursiveChunker
from backend.rag_engine.models.document import Document

doc = Document(
    content="""
    
    This is paragraph one.

This is paragraph two. It contains multiple sentences.
This is another sentence.

This is paragraph three.
    
    
    
    """,
    source="sample.txt",
    file_type="txt",
)

chunker = RecursiveChunker(
    chunk_size=100,
    chunk_overlap=20,
)

chunks = chunker.chunk(doc)

for chunk in chunks:
    print("-" * 40)
    print(chunk.chunk_number)
    print(chunk.content)
