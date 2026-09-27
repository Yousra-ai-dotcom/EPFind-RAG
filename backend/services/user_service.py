"""
Service de gestion des utilisateurs EPFind.
"""

from sqlalchemy.orm import Session

from backend.database.models import User


def get_or_create_user(
    db: Session,
    microsoft_user: dict,
) -> User:
    """
    Récupère l'utilisateur PostgreSQL correspondant au compte Microsoft.
    Le crée automatiquement s'il n'existe pas encore.
    """

    microsoft_id = microsoft_user.get("microsoft_id")
    email = microsoft_user.get("email")
    name = microsoft_user.get("name", "")

    if not microsoft_id:
        raise ValueError("Identifiant Microsoft manquant.")

    if not email:
        raise ValueError("Adresse email Microsoft manquante.")

    user = (
        db.query(User)
        .filter(User.microsoft_id == microsoft_id)
        .first()
    )

    if user is not None:
        return user

    user = User(
        microsoft_id=microsoft_id,
        email=email,
        name=name or email,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user