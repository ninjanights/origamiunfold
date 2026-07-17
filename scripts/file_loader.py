from rag_engine.ingestion.loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load("dataset/raw/samplepdf.pdf")

for doc in documents:
    print(doc)
