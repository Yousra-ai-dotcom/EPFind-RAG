"""
Service RAG principal d'EPFind.

Ce service orchestre la recherche des passages pertinents
et la génération de la réponse finale.
"""

from backend.services.search_service import search_course_content
from generation.answer import build_answer


def answer_question(
    question: str,
    module: str | None = None,
    course: str | None = None,
    top_k: int = 5,
) -> dict:
    """
    Génère une réponse à une question en utilisant le pipeline RAG.

    1. Recherche les passages pertinents dans Azure AI Search.
    2. Transmet ces passages au module de génération.
    3. Retourne la réponse générée avec ses sources.
    """

    if not question or not question.strip():
        raise ValueError("La question ne peut pas être vide.")

    chunks = search_course_content(
        question=question,
        module=module,
        course=course,
        top_k=top_k,
    )

    result = build_answer(
        question=question,
        chunks=chunks,
    )

    return result