"""
Personne 1 — Ingestion
Rôle : lire les fichiers PDF des cours et en extraire le texte brut, page par page.

Entrée attendue : un chemin vers un PDF (local ou téléchargé depuis Azure Blob Storage)
Sortie attendue : une liste de dicts {"page": int, "text": str}
"""

from pathlib import Path


def load_pdf(pdf_path: str) -> list[dict]:
    """
    TODO (Personne 1) :
    - Ouvrir le PDF avec PyMuPDF (fitz)
    - Parcourir chaque page
    - Retourner [{"page": numero_page, "text": texte_brut}, ...]
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Exemple d'utilisation pour tester en local
    pages = load_pdf("../data/courses/exemple.pdf")
    print(pages[:1])
