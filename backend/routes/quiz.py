"""
Route POST /quiz
Responsable principal : Personne 3 (génération), Personne 2 (route + stockage résultats)
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class QuizRequest(BaseModel):
    course: str
    level: str = "facile"
    n_questions: int = 10
    quiz_type: str = "qcm"  # "qcm" ou "vrai_faux"


@router.post("/quiz")
def create_quiz(request: QuizRequest):
    """
    TODO (Personne 3 + Personne 2) :
    - Récupérer le contenu du cours (search.retrieval)
    - Appeler generation.quiz_generator.generate_quiz(...)
    - Retourner la liste de questions au frontend
    """
    raise NotImplementedError


@router.post("/quiz/{quiz_id}/submit")
def submit_quiz(quiz_id: int):
    """
    TODO (Personne 2) :
    - Comparer les réponses de l'utilisateur aux bonnes réponses
    - Enregistrer le score dans PostgreSQL
    - Retourner le score + détail correct/incorrect
    """
    raise NotImplementedError
