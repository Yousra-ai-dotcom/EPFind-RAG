"""
Route POST /summarize
Génère une fiche de révision à partir du contenu d'un cours.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.rag_service import summarize_course

router = APIRouter()


class SummarizeRequest(BaseModel):
    course: str
    summary_type: str = "resume_rapide"
    # valeurs possibles : resume_rapide, resume_detaille, points_cles,
    # fiche_de_revision, explication_pedagogique


@router.post("/summarize")
def summarize(request: SummarizeRequest):
    return summarize_course(request.course, request.summary_type)
