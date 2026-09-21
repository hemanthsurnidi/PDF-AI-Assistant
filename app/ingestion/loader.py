import pymupdf


def load_pdf(file_path):
    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()
        pages.append({
            "page": page_number + 1,
            "text": text
        })

    document.close()

    return pages

if __name__ == "__main__":
    pdf_path = "data/documents/sample.pdf"

    pages = load_pdf(pdf_path)

    print(f"Total pages: {len(pages)}")

    for page in pages:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"][:500])