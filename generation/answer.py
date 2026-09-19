"""
Personne 3 — Prompt + LLM
Rôle : assembler question + contexte récupéré (Personne 2) en une réponse finale
avec ses sources.
"""

from generation.prompts import QA_PROMPT
from generation.llm import call_llm


def build_answer(question: str, chunks: list[dict]) -> dict:
    """
    TODO (Personne 3) :
    - Construire le contexte à partir de `chunks` (concaténation des textes)
    - Remplir QA_PROMPT avec context + question
    - Appeler call_llm()
    - Retourner {"answer": "...", "sources": [{"course":..., "chapter":..., "page":...}, ...]}
    """
    raise NotImplementedError
