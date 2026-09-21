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
    course: str,
    module: str,
    chapter: str,
    page: int,
    document: str,
) -> dict:
    """
    Associe un chunk de texte à ses métadonnées.

    Args:
        chunk_text: Texte du chunk.
        course: Nom du cours.
        module: Nom du module.
        chapter: Nom du chapitre.
        page: Numéro de la page.
        document: Nom du fichier PDF.

    Returns:
        Un dictionnaire contenant le texte et ses métadonnées.
    """

    return {
        "course": course,
        "module": module,
        "chapter": chapter,
        "page": page,
        "document": document,
        "text": chunk_text,
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