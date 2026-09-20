"""
Prompt + LLM
Rôle : générer des QCM structurés (JSON) à partir du contenu d'un cours.
"""

import json

from generation.prompts import QUIZ_PROMPT
from generation.llm import call_llm


def generate_quiz(course_content: str, n_questions: int = 10, level: str = "facile") -> list[dict]:
    prompt = QUIZ_PROMPT.format(
        context=course_content,
        n_questions=n_questions,
        level=level,
    )

    raw_response = call_llm(prompt, temperature=0.5)

    try:
        questions = json.loads(raw_response)
    except json.JSONDecodeError:
        raise ValueError(
            "Le modele n'a pas renvoye un JSON valide : " + raw_response
        )

    return questions
