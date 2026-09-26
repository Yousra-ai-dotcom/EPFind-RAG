"""
Route POST /summarize
Responsable : Personne 3 (génération du résumé) + Personne 2 (route)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.revision_service import generate_summary

router = APIRouter()


class SummarizeRequest(BaseModel):
    course: str
    module: str | None = None
    summary_type: str = "resume_rapide"
    # valeurs possibles : resume_rapide, resume_detaille, points_cles,
    # fiche_de_revision, explication_pedagogique


@router.post("/summarize")
def summarize(request: SummarizeRequest):
    try:
        return generate_summary(
            course=request.course,
            summary_type=request.summary_type,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la génération de la fiche de révision : {str(error)}",
        )
