"""
Routes GET /history et GET /history/{conversation_id}
Responsable : Personne 2
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/history")
def get_history():
    """
    TODO (Personne 2) :
    - Retourner la liste des conversations de l'utilisateur connecté (groupées par date)
    """
    raise NotImplementedError


@router.get("/history/{conversation_id}")
def get_conversation(conversation_id: int):
    """
    TODO (Personne 2) :
    - Retourner tous les messages d'une conversation donnée
    """
    raise NotImplementedError
