"""
Service de gestion de l'historique des conversations EPFind.
"""

from sqlalchemy.orm import Session

from backend.database.models import Conversation, Message


def create_conversation(
    db: Session,
    title: str,
    user_id: int | None = None,
) -> Conversation:
    """Crée une nouvelle conversation."""

    conversation = Conversation(
        user_id=user_id,
        title=title[:255],
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    """Ajoute un message à une conversation."""

    if role not in {"user", "assistant"}:
        raise ValueError("Le rôle doit être 'user' ou 'assistant'.")

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if conversation is None:
        raise ValueError(
            f"La conversation {conversation_id} n'existe pas."
        )

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversations(
    db: Session,
    user_id: int | None = None,
) -> list[Conversation]:
    """Retourne les conversations, de la plus récente à la plus ancienne."""

    query = db.query(Conversation)

    if user_id is not None:
        query = query.filter(Conversation.user_id == user_id)

    return query.order_by(
        Conversation.created_at.desc()
    ).all()


def get_conversation_by_id(
    db: Session,
    conversation_id: int,
) -> Conversation | None:
    """Retourne une conversation et ses messages."""

    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )