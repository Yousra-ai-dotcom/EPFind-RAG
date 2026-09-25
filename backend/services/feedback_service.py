"""
Service Feedback (like/dislike) d'EPFind.
Responsable : Personne 3.

Comme il n'y a pas encore de base de données PostgreSQL branchée,
on garde les retours en mémoire pour le MVP (même logique que
_quizzes dans quiz_service.py). A remplacer plus tard par une vraie
table si Personne 2 termine backend/database avant la présentation.
"""

_feedbacks: list[dict] = []


def save_feedback(question: str, answer: str, liked: bool, reason: str | None = None) -> dict:
    entry = {
        "question": question,
        "answer": answer,
        "liked": liked,
        "reason": reason,
    }
    _feedbacks.append(entry)
    return entry


def list_feedbacks() -> list[dict]:
    """Utile pour debug / démo : voir tous les retours reçus pendant la session."""
    return _feedbacks
