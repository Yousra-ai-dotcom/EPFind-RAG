"""
Route POST /ask
Reçoit une question, appelle le RAG (search + generation), enregistre
l'échange en base et retourne la réponse + les sources.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.auth.entra import get_current_user_optional
from backend.services.rag_service import ask_rag, get_or_create_user

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
def ask(
    request: AskRequest,
    db: Session = Depends(get_db),
    identity: dict = Depends(get_current_user_optional),
):
    user = get_or_create_user(db, identity)
    result = ask_rag(
        db=db,
        user=user,
        question=request.question,
        course=request.course,
        conversation_id=request.conversation_id,
    )
    return result
