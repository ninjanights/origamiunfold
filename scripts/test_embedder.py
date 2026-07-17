from rag_engine.embeddings.bge_embedder import BGEEmbedder
from rag_engine.models.chunk import Chunk

chunks = [
    Chunk(
        id="1",
        content="Python is awesome.",
        source="sample.txt",
        file_type="txt",
    ),
    Chunk(
        id="2",
        content="Machine learning uses embeddings.",
        source="sample.txt",
        file_type="txt",
    ),
]
chunks2 = [
    Chunk(
        id="1",
        content="Tesla",
        source="sample.txt",
        file_type="txt",
    )
]

embedder1 = BGEEmbedder()
embedder2 = BGEEmbedder()

vector = embedder1.embed_chunks(chunks)

vector2 = embedder2.embed_chunks(chunks2)

print(len(vector))
print(len(vector2))

print(len(vector[0]))
print(embedder1.model is embedder2.model)
print(len(vector2[0]))
