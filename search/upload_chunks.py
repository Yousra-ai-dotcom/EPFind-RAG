"""
Envoie les chunks d'un PDF vers Azure AI Search
avec leurs embeddings Azure OpenAI.
"""

from pathlib import Path
import uuid

from ingestion.pipeline import process_pdf
from search.embeddings import get_embeddings_batch
from search.index import upload_documents


def upload_pdf_to_search(pdf_path: str) -> None:
    # 1. Extraire les chunks du PDF
    chunks = process_pdf(pdf_path)

    if not chunks:
        print("Aucun chunk trouvé.")
        return

    print(f"{len(chunks)} chunks trouvés.")

    # 2. Extraire les textes
    texts = [chunk["text"] for chunk in chunks]

    # 3. Générer les embeddings
    print("Génération des embeddings...")

    embeddings = get_embeddings_batch(texts)

    print(f"{len(embeddings)} embeddings générés.")

    # 4. Préparer les documents pour Azure AI Search
    documents = []

    for chunk, embedding in zip(chunks, embeddings):

        document_name = chunk["document"]

        document = {
            "id": str(uuid.uuid4()),
            "course_id": Path(document_name).stem,
            "course_name": Path(document_name).stem,
            "module": "",
            "chapter": "",
            "page": chunk["page"],
            "content": chunk["text"],
            "content_vector": embedding,
            "document_name": document_name,
        }

        documents.append(document)

    # 5. Envoyer vers Azure AI Search
    print("Upload vers Azure AI Search...")

    upload_documents(documents)

    print("Upload terminé avec succès !")


if __name__ == "__main__":
    upload_pdf_to_search(
        "data/courses/cours-01.pdf"
    )
