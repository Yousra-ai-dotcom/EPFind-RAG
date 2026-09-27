"""
Personne 1 — Ingestion

Rôle : associer à chaque chunk ses métadonnées (cours, module, chapitre, page).

Format attendu pour un chunk final (envoyé ensuite à Personne 2 pour l'embedding) :
{
    "course": "Machine Learning",
    "module": "Artificial Intelligence",
    "chapter": "Regression",
    "page": 12,
    "document": "cours-01.pdf",
    "text": "La régression linéaire est une méthode..."
}
"""


def attach_metadata(
    chunk_text: str,
    page: int,
    document: str,
    module: str = "",
    course: str = "",
) -> dict:
    """
    Attach metadata to a text chunk.
    """

    return {
        "text": chunk_text,
        "module": module,
        "course": course,
        "page": page,
        "document": document,
    }
