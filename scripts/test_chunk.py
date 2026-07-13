from backend.rag_engine.models.chunk import Chunk

chunk = Chunk(
    id="chunk_1",
    content="Hello World",
    source="sample.txt",
    file_type="txt",
    chunk_number=1,
)

print(chunk)