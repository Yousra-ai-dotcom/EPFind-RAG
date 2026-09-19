"""
Route GET /courses
Responsable : Personne 2

Retourne la liste des cours disponibles (pour remplir le sélecteur de cours
côté frontend).
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/courses")
def get_courses():
    """
    TODO (Personne 2) :
    - Retourner la liste des cours distincts présents dans l'index Azure AI Search
      (ou une table `courses` dédiée en base si vous préférez la figer)
    """
    raise NotImplementedError
