"""
Personne 1 — Pipeline d'ingestion

Pipeline complet :

PDF
 ↓
Extraction du texte
 ↓
Nettoyage
 ↓
Découpage en chunks
 ↓
Ajout des métadonnées

Le résultat est une liste de chunks prêts à être
envoyés à Personne 2 pour les embeddings.
"""

from ingestion.pdf_loader import load_pdf
from ingestion.cleaner import clean_text
from ingestion.chunker import chunk_text
from ingestion.metadata import attach_metadata


def process_pdf(
    pdf_path: str,
    course: str,
    module: str,
    chapter: str,
    document: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """
    Traite un PDF de bout en bout.

    Args:
        pdf_path: chemin vers le fichier PDF.
        course: nom du cours.
        module: nom du module.
        chapter: nom du chapitre.
        document: nom du document.
        chunk_size: nombre de mots maximum par chunk.
        overlap: nombre de mots partagés entre deux chunks.

    Returns:
        Liste de dictionnaires contenant :
        - course
        - module
        - chapter
        - page
        - document
        - text
    """

    # 1. Extraction du PDF
    pages = load_pdf(pdf_path)

    final_chunks = []

    # 2. Traiter chaque page
    for page_data in pages:
        page_number = page_data["page"]
        raw_text = page_data["text"]

        # 3. Nettoyage
        cleaned_text = clean_text(raw_text)

        # Ignorer les pages vides
        if not cleaned_text:
            continue

        # 4. Découpage en chunks
        chunks = chunk_text(
            cleaned_text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        # 5. Ajouter les métadonnées à chaque chunk
        for chunk in chunks:
            chunk_with_metadata = attach_metadata(
                chunk_text=chunk,
                course=course,
                module=module,
                chapter=chapter,
                page=page_number,
                document=document,
            )

            final_chunks.append(chunk_with_metadata)

    return final_chunks


if __name__ == "__main__":
    print("Pipeline d'ingestion chargé correctement.")
    print()
    print("Utilisation :")
    print(
        "process_pdf("
        '"chemin/vers/fichier.pdf", '
        '"Machine Learning", '
        '"Artificial Intelligence", '
        '"Regression", '
        '"cours-01.pdf"'
        ")"
    )