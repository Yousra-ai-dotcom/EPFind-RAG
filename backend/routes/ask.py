"""
Route POST /ask

Reçoit une question depuis le frontend,
appelle le pipeline RAG, sauvegarde la conversation
et retourne la réponse générée avec ses sources.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.auth.entra import get_current_user
from backend.services.user_service import get_or_create_user
from backend.database.database import get_db
from backend.services.history_service import (
    add_message,
    create_conversation,
    get_conversation_by_id,
)
from backend.services.rag_service import answer_question


router = APIRouter()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    module: str | None = None
    course: str | None = None
    conversation_id: int | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[dict]
    conversation_id: int


@router.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
    db: Session = Depends(get_db),
    microsoft_user: dict = Depends(get_current_user),
):
    """
    Answer a question using the EPFind RAG pipeline
    and save the conversation in PostgreSQL.
    """

    try:
        user = get_or_create_user(
            db=db,
            microsoft_user=microsoft_user,
        )
        # 1. Nouvelle conversation ou conversation existante
        if request.conversation_id is None:
            conversation = create_conversation(
                db=db,
                title=request.question,
                user_id=user.id,
            )
        else:
            conversation = get_conversation_by_id(
                db=db,
                conversation_id=request.conversation_id,
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

        # 2. Génération RAG
        result = answer_question(
            question=request.question,
            module=request.module,
            course=request.course,
        )

        # 3. Sauvegarde de la question
        add_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content=request.question,
        )

        # 4. Sauvegarde de la réponse
        add_message(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=result["answer"],
        )

        # 5. Réponse envoyée au frontend
        return AskResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=conversation.id,
        )

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la génération de la réponse : {str(error)}",
        )