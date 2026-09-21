"""
Personne 1 — Ingestion
Rôle : lire les fichiers PDF des cours et en extraire le texte brut, page par page.

Entrée attendue : un chemin vers un PDF (local ou téléchargé depuis Azure Blob Storage)
Sortie attendue : une liste de dicts {"page": int, "text": str}
"""

from pathlib import Path

import pymupdf


def load_pdf(pdf_path: str) -> list[dict]:
    """
    Ouvre un PDF et extrait son texte page par page.

    Args:
        pdf_path: Chemin vers le fichier PDF.

    Returns:
        Liste de dictionnaires contenant le numéro de page
        et le texte extrait.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf_path}")

    if not path.is_file():
        raise ValueError(f"Le chemin n'est pas un fichier : {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Le fichier n'est pas un PDF : {pdf_path}")

    pages = []

    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append({
                "page": page_number,
                "text": text,
            })

    return pages


if __name__ == "__main__":
    pages = load_pdf("../data/courses/exemple.pdf")
    print(pages[:1])