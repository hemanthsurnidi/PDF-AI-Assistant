import re


def chunk_pages(pages, chunk_size=1000, chunk_overlap=200):
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        sentences = re.split(r'(?<=[.!?])\s+', text)

        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "page": page_number
                    })

                overlap_text = current_chunk[-chunk_overlap:]
                current_chunk = overlap_text + sentence + " "

        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "page": page_number
            })

    return chunks

if __name__ == "__main__":
    from app.ingestion.loader import load_pdf

    pages = load_pdf("data/documents/sample.pdf")
    chunks = chunk_pages(pages)

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:3], start=1):
        print(f"\n--- Chunk {i} | Page {chunk['page']} ---")
        print(chunk["text"])