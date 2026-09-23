"""
Route POST /quiz
Génère un QCM à partir du contenu d'un cours, et permet de soumettre les
réponses de l'utilisateur pour obtenir un score.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Quiz
from backend.auth.entra import get_current_user_optional
from backend.services.rag_service import create_quiz_for_course, get_or_create_user

router = APIRouter()


class QuizRequest(BaseModel):
    course: str
    level: str = "facile"
    n_questions: int = 10
    quiz_type: str = "qcm"  # "qcm" ou "vrai_faux"


class QuizSubmitRequest(BaseModel):
    answers: list[int]  # index choisi par l'utilisateur, pour chaque question


@router.post("/quiz")
def create_quiz(
    request: QuizRequest,
    db: Session = Depends(get_db),
    identity: dict = Depends(get_current_user_optional),
):
    try:
        questions = create_quiz_for_course(
            request.course, request.level, request.n_questions
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    user = get_or_create_user(db, identity)

    quiz = Quiz(
        user_id=user.id,
        course=request.course,
        level=request.level,
        questions_json=json.dumps(questions),
        number_questions=len(questions),
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return {"quiz_id": quiz.id, "questions": questions}


@router.post("/quiz/{quiz_id}/submit")
def submit_quiz(
    quiz_id: int,
    request: QuizSubmitRequest,
    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable")

    questions = json.loads(quiz.questions_json)

    correct_count = 0
    details = []
    for i, question in enumerate(questions):
        user_answer = request.answers[i] if i < len(request.answers) else None
        is_correct = user_answer == question["correct_answer"]
        if is_correct:
            correct_count += 1
        details.append({
            "question": question["question"],
            "correct": is_correct,
            "correct_answer": question["correct_answer"],
            "explanation": question.get("explanation"),
        })

    score_percent = round(100 * correct_count / len(questions), 1) if questions else 0

    quiz.score = score_percent
    db.commit()

    return {
        "score": correct_count,
        "total": len(questions),
        "score_percent": score_percent,
        "details": details,
    }
