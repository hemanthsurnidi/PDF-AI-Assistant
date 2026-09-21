from sentence_transformers import SentenceTransformer

from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_pages
from app.retrieval.retriever import add_documents


model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    return model.encode(
        texts,
        convert_to_numpy=True
    )


def ingest_pdf(file_path, filename):

    pages = load_pdf(file_path)

    if not pages:
        raise ValueError("PDF contains no readable pages.")

    chunks = chunk_pages(pages)

    if not chunks:
        raise ValueError("PDF produced no usable text chunks.")

    embeddings = embed_chunks(chunks)

    count = add_documents(
        chunks,
        embeddings,
        filename
    )

    return count