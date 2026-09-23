"""
Routes GET /history et GET /history/{conversation_id}
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Conversation, Message
from backend.auth.entra import get_current_user_optional
from backend.services.rag_service import get_or_create_user

router = APIRouter()


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    identity: dict = Depends(get_current_user_optional),
):
    user = get_or_create_user(db, identity)
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
    return {
        "conversations": [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at.isoformat(),
            }
            for c in conversations
        ]
    }


@router.get("/history/{conversation_id}")
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return {
        "id": conversation.id,
        "title": conversation.title,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "sources": m.sources,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ],
    }
