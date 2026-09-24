from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.quiz_service import (
    generate_quiz_for_course,
    save_quiz,
    grade_quiz,
)
router = APIRouter()


class QuizRequest(BaseModel):
    course: str
    level: str = "facile"
    n_questions: int = 10
    quiz_type: str = "qcm"


@router.post("/quiz")
def create_quiz(request: QuizRequest):
    """
    Génère un QCM à partir du cours sélectionné.
    """

    try:
        questions = generate_quiz_for_course(
            course=request.course,
            level=request.level,
            n_questions=request.n_questions,
        )

        quiz_id = save_quiz(questions)

        return {
            "quiz_id": quiz_id,
            "questions": questions,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la génération du QCM : {str(error)}",
        )

class QuizSubmitRequest(BaseModel):
    answers: list[int]


@router.post("/quiz/{quiz_id}/submit")
def submit_quiz(
    quiz_id: int,
    request: QuizSubmitRequest,
):
    """
    Corrige les réponses d'un QCM.
    """

    try:
        return grade_quiz(
            quiz_id=quiz_id,
            user_answers=request.answers,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la correction du QCM : {str(error)}",
        )