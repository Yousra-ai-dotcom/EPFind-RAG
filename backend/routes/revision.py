"""
Route POST /summarize

Reçoit un cours et un type de révision,
puis génère le contenu correspondant.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.revision_service import generate_course_summary

router = APIRouter()


class SummarizeRequest(BaseModel):
    course: str
    summary_type: str = "resume_rapide"


@router.post("/summarize")
def summarize(request: SummarizeRequest):
    """
    Génère un contenu de révision à partir d'un cours indexé.

    Types disponibles :
    - resume_rapide
    - resume_detaille
    - points_cles
    - fiche_de_revision
    - explication_pedagogique
    """

    try:
        summary = generate_course_summary(
            course=request.course,
            summary_type=request.summary_type,
        )

        return {
            "summary": summary,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la génération de la révision : {str(error)}",
        )