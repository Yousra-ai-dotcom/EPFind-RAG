"""
Route POST /feedback
Reçoit un like/dislike de l'étudiant sur une réponse du Chat.
Responsable : Personne 3.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.feedback_service import save_feedback

router = APIRouter()


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    liked: bool
    reason: str | None = None  # rempli seulement si liked = False


@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    saved = save_feedback(
        question=request.question,
        answer=request.answer,
        liked=request.liked,
        reason=request.reason,
    )
    return {"status": "ok", "feedback": saved}
