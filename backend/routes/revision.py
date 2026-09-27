"""
Route POST /summarize
Responsable : Personne 3 (génération du résumé) + Personne 2 (route)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.revision_service import generate_summary
from backend.services.activity_log import log_activity

router = APIRouter()


class SummarizeRequest(BaseModel):
    course: str
    module: str | None = None
    summary_type: str = "resume_rapide"


@router.post("/summarize")
def summarize(request: SummarizeRequest):
    try:
        result = generate_summary(
            course=request.course,
            summary_type=request.summary_type,
        )
        log_activity(
            activity_type="revision",
            title=f"Révision — {request.course}",
            module=request.module,
            course=request.course,
        )
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la génération de la fiche de révision : {str(error)}",
        )
