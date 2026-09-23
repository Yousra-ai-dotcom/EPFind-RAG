"""
Service central du RAG — relie retrieval (Personne 2) et génération (Personne 3).
C'est la fonction que les routes /ask, /summarize, /quiz appellent en interne.
"""

import json
from sqlalchemy.orm import Session

from search.retrieval import retrieve, retrieve_full_course
from generation.answer import build_answer
from generation.prompts import SUMMARY_PROMPT
from generation.llm import call_llm
from generation.quiz_generator import generate_quiz
from backend.database.models import User, Conversation, Message


def get_or_create_user(db: Session, identity: dict) -> User:
    """Retrouve l'utilisateur en base à partir de son identité Microsoft,
    ou le crée s'il se connecte pour la première fois."""
    user = db.query(User).filter(User.microsoft_id == identity["microsoft_id"]).first()
    if user:
        return user

    user = User(
        name=identity.get("name") or "Étudiant EPF",
        email=identity["email"],
        microsoft_id=identity["microsoft_id"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ask_rag(
    db: Session,
    user: User,
    question: str,
    course: str | None = None,
    conversation_id: int | None = None,
) -> dict:
    """
    Pipeline complet d'une question :
    question -> recherche RAG -> réponse LLM -> sauvegarde -> retour au frontend
    """
    # 1. Recherche des passages pertinents dans les cours
    chunks = retrieve(question, course=course)

    # 2. Génération de la réponse à partir des passages trouvés
    result = build_answer(question, chunks)

    # 3. Récupère la conversation existante ou en crée une nouvelle
    if conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id, Conversation.user_id == user.id
        ).first()
    else:
        conversation = None

    if not conversation:
        title = question[:50] + ("..." if len(question) > 50 else "")
        conversation = Conversation(user_id=user.id, title=title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 4. Sauvegarde des deux messages (question + réponse) dans l'historique
    db.add(Message(conversation_id=conversation.id, role="user", content=question))
    db.add(Message(
        conversation_id=conversation.id,
        role="assistant",
        content=result["answer"],
        sources=json.dumps(result["sources"]),
    ))
    db.commit()

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "conversation_id": conversation.id,
    }


def summarize_course(course: str, summary_type: str) -> dict:
    """Génère une fiche de révision à partir de tout le contenu d'un cours."""
    chunks = retrieve_full_course(course)

    if not chunks:
        return {"summary": "Aucun contenu trouvé pour ce cours dans les cours indexés."}

    context = "\n\n".join(chunk["text"] for chunk in chunks if chunk.get("text"))
    prompt = SUMMARY_PROMPT.format(course=course, context=context)
    summary_text = call_llm(prompt)

    return {"summary": summary_text}


def create_quiz_for_course(course: str, level: str, n_questions: int) -> list[dict]:
    """Génère un QCM à partir du contenu d'un cours."""
    chunks = retrieve_full_course(course)

    if not chunks:
        raise ValueError(f"Aucun contenu trouvé pour le cours '{course}'.")

    context = "\n\n".join(chunk["text"] for chunk in chunks if chunk.get("text"))
    return generate_quiz(context, n_questions=n_questions, level=level)
