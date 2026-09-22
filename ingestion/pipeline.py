from pathlib import Path

from ingestion.pdf_loader import load_pdf
from ingestion.cleaner import clean_text
from ingestion.chunker import chunk_text
from ingestion.metadata import attach_metadata


def process_pdf(pdf_path):
    pages = load_pdf(pdf_path)

    all_chunks = []

    for page in pages:
        text = clean_text(page["text"])

        if not text.strip():
            continue

        chunks = chunk_text(text)

        for chunk in chunks:
            chunk_with_metadata = attach_metadata(
            chunk_text=chunk,
            page=page["page"],
            document=Path(pdf_path).name,
            )

            all_chunks.append(chunk_with_metadata)

    return all_chunks


if __name__ == "__main__":
    chunks = process_pdf("data/courses/cours-01.pdf")

    print("Nombre de chunks :", len(chunks))

    if chunks:
        print("\nPremier chunk :")
        print(chunks[0])