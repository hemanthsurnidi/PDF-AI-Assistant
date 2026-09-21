from app.retrieval.retriever import (
    create_query_embedding,
    search
)

from app.llm.generator import generate_answer


def ask_question(question, top_k=3):

    query_embedding = create_query_embedding(
        question
    )

    results = search(
        query_embedding,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        context_parts.append(
            f"[File: {metadata['filename']} | "
            f"Page: {metadata['page']}]\n"
            f"{document}"
        )

    context = "\n\n".join(
        context_parts
    )

    answer = generate_answer(
        context,
        question
    )

    sources = []
    seen = set()

    for document, metadata in zip(
        documents,
        metadatas
    ):

        key = (
            metadata["filename"],
            metadata["page"]
        )

        if key not in seen:

            sources.append({
                "filename": metadata["filename"],
                "page": metadata["page"],
                "text": document
            })

            seen.add(key)

    return answer, sources