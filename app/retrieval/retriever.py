import hashlib

import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="vectorstore"
)


def get_collection():
    return client.get_or_create_collection(
        name="documents"
    )


def create_document_id(filename):
    return hashlib.sha256(
        filename.encode("utf-8")
    ).hexdigest()[:12]


def add_documents(chunks, embeddings, filename):

    collection = get_collection()

    document_id = create_document_id(filename)

    # Check whether this document is already indexed
    existing = collection.get(
        where={
            "filename": filename
        }
    )

    if existing["ids"]:
        return 0

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "filename": filename,
            "document_id": document_id,
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return len(chunks)


def create_query_embedding(query):
    return model.encode(query)


def search(query_embedding, top_k=3):

    collection = get_collection()

    return collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )