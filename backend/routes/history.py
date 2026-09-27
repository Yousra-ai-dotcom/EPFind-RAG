"""
Routes de gestion de l'historique des conversations EPFind.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.services.history_service import (
    get_conversation_by_id,
    get_conversations,
)
from backend.auth.entra import get_current_user
from backend.services.user_service import get_or_create_user

router = APIRouter()


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    microsoft_user: dict = Depends(get_current_user),
):
    """
    Retourne les conversations de l'utilisateur connecté.
    """

    user = get_or_create_user(
        db=db,
        microsoft_user=microsoft_user,
    )

    conversations = get_conversations(
        db=db,
        user_id=user.id,
    )

    return [
        {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
        }
        for conversation in conversations
    ]


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