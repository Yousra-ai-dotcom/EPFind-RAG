"""
Journal d'activité pour la Révision et le QCM.

Le Chat a déjà un vrai historique en base PostgreSQL (Conversation/Message,
géré par Yousra dans history_service.py). La Révision et le QCM n'ont pas
de table dédiée pour le moment : on garde donc une trace légère en mémoire
(perdue si le serveur redémarre - acceptable pour le MVP du hackathon),
pour pouvoir les afficher dans la page Historique à côté du Chat.
"""

from datetime import datetime

_activities: list[dict] = []


def log_activity(activity_type: str, title: str, module: str | None = None, course: str | None = None):
    """activity_type : 'revision' ou 'quiz'"""
    _activities.append({
        "type": activity_type,
        "title": title,
        "module": module,
        "course": course,
        "created_at": datetime.utcnow().isoformat(),
    })


def get_activities(activity_type: str | None = None) -> list[dict]:
    if activity_type:
        return [a for a in _activities if a["type"] == activity_type]
    return list(_activities)
