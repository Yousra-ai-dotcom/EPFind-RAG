"""
Route POST /summarize
Responsable : Personne 3 (génération du résumé) + Personne 2 (route)
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SummarizeRequest(BaseModel):
    course: str
    summary_type: str = "resume_rapide"
    # valeurs possibles : resume_rapide, resume_detaille, points_cles,
    # fiche_de_revision, explication_pedagogique


@router.post("/summarize")
def summarize(request: SummarizeRequest):
    """
    TODO (Personne 3 + Personne 2) :
    - Récupérer le contenu du cours via search.retrieval
    - Générer la fiche de révision via generation (prompt SUMMARY_PROMPT)
    - Retourner le résultat
    """
    raise NotImplementedError
