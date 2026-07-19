import chromadb

client = chromadb.PersistentClient(
    path="./storage/chroma"
)

collection = client.get_collection(
    "origamidocuments"
)

print("Total documents:", collection.count())

data = collection.get(
    limit=3
)

print(data)