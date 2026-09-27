from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.quiz_service import (
    generate_quiz_for_course,
    save_quiz,
    grade_quiz,
)
from backend.services.activity_log import log_activity

router = APIRouter()


class QuizRequest(BaseModel):
    course: str
    module: str | None = None
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

        log_activity(
            activity_type="quiz",
            title=f"QCM — {request.course} ({request.level})",
            module=request.module,
            course=request.course,
        )

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
