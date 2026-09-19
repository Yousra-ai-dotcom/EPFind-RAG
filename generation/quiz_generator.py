"""
Personne 3 — Prompt + LLM
Rôle : générer des QCM structurés (JSON) à partir du contenu d'un cours.
"""

import json

from generation.prompts import QUIZ_PROMPT
from generation.llm import call_llm


def generate_quiz(course_content: str, n_questions: int = 10, level: str = "facile") -> list[dict]:
    """
    TODO (Personne 3) :
    - Remplir QUIZ_PROMPT avec le contenu du cours
    - Appeler call_llm()
    - Parser la réponse JSON (json.loads) et la valider
    - Retourner la liste de questions au format attendu par le frontend
    """
    raise NotImplementedError
