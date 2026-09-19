"""
Service central du RAG — relie retrieval (Personne 2) et génération (Personne 3).
Responsable : Personne 2 (intégration)

C'est la fonction que les routes /ask, /summarize, /quiz appellent en interne.
"""

from search.retrieval import retrieve
from generation.answer import build_answer


def ask_rag(question: str, course: str | None = None, conversation_id: int | None = None) -> dict:
    """
    TODO (Personne 2) :
    - chunks = retrieve(question, course)
    - result = build_answer(question, chunks)
    - Enregistrer en base (via services/... ou database/models.py)
    - Retourner {"answer":..., "sources":..., "conversation_id":...}
    """
    raise NotImplementedError
