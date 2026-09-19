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
    TODO (Personne 1) :
    - Construire et retourner le dict de métadonnées ci-dessus
    """
    raise NotImplementedError
