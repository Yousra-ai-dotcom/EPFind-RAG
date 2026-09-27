"""
Routes de gestion de l'historique EPFind :
Chat (base de données), Révision et QCM (journal d'activité).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.entra import get_current_user
from backend.database.database import get_db
from backend.services.activity_log import get_activities
from backend.services.history_service import (
    get_conversation_by_id,
    get_conversations,
)
from backend.services.user_service import get_or_create_user

router = APIRouter()


@router.get("/history")
def get_history(
    type: str | None = None,
    db: Session = Depends(get_db),
    microsoft_user: dict = Depends(get_current_user),
):
    """
    Retourne l'historique de l'utilisateur connecté.

    `type` peut valoir "chat", "revision", "quiz"
    ou être omis pour tout récupérer.
    """

    user = get_or_create_user(
        db=db,
        microsoft_user=microsoft_user,
    )

    items = []

    if type in (None, "chat"):
        conversations = get_conversations(
            db=db,
            user_id=user.id,
        )

        items += [
            {
                "type": "chat",
                "id": c.id,
                "title": c.title,
                "created_at": (
                    c.created_at.isoformat()
                    if hasattr(c.created_at, "isoformat")
                    else c.created_at
                ),
            }
            for c in conversations
        ]

    if type in (None, "revision"):
        items += [
            {**a, "id": None}
            for a in get_activities("revision")
        ]

    if type in (None, "quiz"):
        items += [
            {**a, "id": None}
            for a in get_activities("quiz")
        ]

    items.sort(
        key=lambda item: item["created_at"],
        reverse=True,
    )

    return {"conversations": items}


@router.get("/history/{conversation_id}")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    microsoft_user: dict = Depends(get_current_user),
):
    """
    Retourne une conversation avec tous ses messages.
    """

    user = get_or_create_user(
        db=db,
        microsoft_user=microsoft_user,
    )

    conversation = get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation introuvable.",
        )

    if conversation.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Accès interdit à cette conversation.",
        )

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in conversation.messages
        ],
    }
