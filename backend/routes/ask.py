"""
Route POST /ask
Responsable : Personne 2 (route) + Personne 3 (logique RAG/génération)

Reçoit une question, appelle le RAG (search + generation), enregistre
l'échange en base et retourne la réponse + les sources.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AskRequest(BaseModel):
    question: str
    course: str | None = None
    conversation_id: int | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[dict]
    conversation_id: int


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    TODO (Personne 2 + Personne 3) :
    - Appeler search.retrieval.retrieve(question, course)
    - Appeler generation.answer.build_answer(question, chunks)
    - Enregistrer question/réponse dans PostgreSQL (database/models.py)
    - Retourner AskResponse
    """
    raise NotImplementedError
