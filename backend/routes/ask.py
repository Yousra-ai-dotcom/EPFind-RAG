"""
Route POST /ask

Reçoit une question depuis le frontend,
appelle le pipeline RAG et retourne
la réponse générée avec ses sources.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

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
    conversation_id: int | None = None


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    Answer a question using the EPFind RAG pipeline.

    Pipeline:
    question
        -> Azure AI Search
        -> relevant course chunks
        -> Azure OpenAI
        -> answer + sources
    """

    try:
        result = answer_question(
            question=request.question,
            module=request.module,
            course=request.course,
        )

        return AskResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=request.conversation_id,
        )

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