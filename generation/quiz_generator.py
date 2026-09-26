"""
Prompt + LLM
Rôle : générer des QCM structurés (JSON) à partir du contenu d'un cours.
"""

import json
import re

from generation.prompts import QUIZ_PROMPT
from generation.llm import call_llm


def _extract_json(raw_text: str) -> str:
    """
    Le modèle répond parfois en entourant le JSON de ```json ... ```.
    Cette fonction nettoie la réponse pour ne garder que le JSON pur.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```json\s*|^```\s*|```$", "", cleaned, flags=re.MULTILINE)
    return cleaned.strip()


def generate_quiz(course_content: str, n_questions: int = 10, level: str = "facile") -> list[dict]:
    prompt = QUIZ_PROMPT.format(
        context=course_content,
        n_questions=n_questions,
        level=level,
    )

    raw_response = call_llm(prompt, temperature=0.5)
    cleaned_response = _extract_json(raw_response)

    try:
        questions = json.loads(cleaned_response)
    except json.JSONDecodeError:
        raise ValueError(
            "Le modèle n'a pas renvoyé un JSON valide : " + raw_response
        )

    return questions
