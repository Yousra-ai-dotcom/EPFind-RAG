"""
Personne 2 — Embeddings + Search
Rôle : rechercher les chunks les plus pertinents pour une question donnée,
avec filtrage optionnel par cours.

Utilisé ensuite par `generation/answer.py` (Personne 3) et par le backend.
"""

from search.embeddings import get_embedding


def retrieve(question: str, course: str | None = None, top_k: int = 5) -> list[dict]:
    """
    TODO (Personne 2) :
    - Calculer l'embedding de `question`
    - Interroger Azure AI Search (recherche vectorielle + hybride texte)
    - Si `course` est fourni, filtrer sur course_name == course
    - Retourner les `top_k` chunks les plus pertinents, avec leurs métadonnées
    """
    raise NotImplementedError
