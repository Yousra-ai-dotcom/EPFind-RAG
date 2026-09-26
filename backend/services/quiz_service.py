"""
Service QCM d'EPFind.

Ce service récupère le contenu d'un cours depuis Azure AI Search
puis utilise le module de génération pour créer un QCM.
"""

from search.retrieval import get_course_content
from generation.quiz_generator import generate_quiz


def generate_quiz_for_course(
    course: str,
    level: str = "facile",
    n_questions: int = 10,
) -> list[dict]:
    """
    Génère un QCM à partir du contenu d'un cours indexé.
    """

    if not course or not course.strip():
        raise ValueError("Le cours doit être précisé.")

    if n_questions < 1 or n_questions > 20:
        raise ValueError(
            "Le nombre de questions doit être compris entre 1 et 20."
        )

    allowed_levels = {"facile", "moyen", "difficile"}

    if level not in allowed_levels:
        raise ValueError(
            "Le niveau doit être facile, moyen ou difficile."
        )

    # Récupération du contenu du cours depuis Azure AI Search
    chunks = get_course_content(
        course=course,
        max_chunks=50,
    )

    if not chunks:
        raise ValueError(
            f"Aucun contenu trouvé pour le cours '{course}'."
        )

    # Construction du contexte envoyé au LLM
    course_content = "\n\n".join(
        chunk["content"]
        for chunk in chunks
        if chunk.get("content")
    )

    if not course_content.strip():
        raise ValueError(
            f"Le cours '{course}' ne contient aucun texte exploitable."
        )

    # Génération du QCM par la partie génération
    questions = generate_quiz(
        course_content=course_content,
        n_questions=n_questions,
        level=level,
    )

    return questions

# Stockage temporaire des quiz en mémoire.
# Pour le MVP du hackathon.
_quizzes: dict[int, list[dict]] = {}
_next_quiz_id = 1


def save_quiz(questions: list[dict]) -> int:
    """
    Enregistre temporairement un QCM et retourne son identifiant.
    """
    global _next_quiz_id

    quiz_id = _next_quiz_id
    _quizzes[quiz_id] = questions
    _next_quiz_id += 1

    return quiz_id


def grade_quiz(
    quiz_id: int,
    user_answers: list[int],
) -> dict:
    """
    Corrige les réponses d'un utilisateur.
    """

    if quiz_id not in _quizzes:
        raise ValueError(f"Quiz {quiz_id} introuvable.")

    questions = _quizzes[quiz_id]

    if len(user_answers) != len(questions):
        raise ValueError(
            "Le nombre de réponses ne correspond pas au nombre de questions."
        )

    score = 0
    details = []

    for index, question in enumerate(questions):
        user_answer = user_answers[index]
        correct_answer = question["correct_answer"]

        is_correct = user_answer == correct_answer

        if is_correct:
            score += 1

        details.append(
            {
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "correct": is_correct,
                "explanation": question.get("explanation", ""),
            }
        )

    return {
        "score": score,
        "total": len(questions),
        "details": details,
    }