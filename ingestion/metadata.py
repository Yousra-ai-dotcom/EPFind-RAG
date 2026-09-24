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
) -> dict:
    """
    Attach basic metadata to a text chunk.

    Module and course metadata are added later
    by the course management / indexing pipeline.
    """

    return {
        "text": chunk_text,
        "page": page,
        "document": document,
    }

    


if __name__ == "__main__":
    # Exemple de test
    chunk = attach_metadata(
        chunk_text="La régression linéaire est une méthode...",
        course="Machine Learning",
        module="Artificial Intelligence",
        chapter="Regression",
        page=12,
        document="cours-01.pdf",
    )

    print(chunk)