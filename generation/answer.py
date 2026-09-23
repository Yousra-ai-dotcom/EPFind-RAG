"""
Personne 3 — Prompt + LLM

Rôle : assembler la question et les chunks récupérés
pour générer une réponse avec ses sources.
"""

from generation.prompts import QA_PROMPT
from generation.llm import call_llm


def build_answer(question: str, chunks: list[dict]) -> dict:
    """
    Construit le contexte RAG, appelle le LLM et retourne
    la réponse avec les sources.
    """

    if not chunks:
        return {
            "answer": "Je ne trouve pas cette information dans les cours.",
            "sources": [],
        }

    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}]\n"
            f"Cours : {chunk.get('course', '')}\n"
            f"Document : {chunk.get('document', '')}\n"
            f"Page : {chunk.get('page', '')}\n"
            f"Contenu :\n{chunk.get('content', '')}"
        )

    context = "\n\n".join(context_parts)

    prompt = QA_PROMPT.format(
        context=context,
        question=question,
    )

    answer = call_llm(prompt)

    sources = [
        {
            "course": chunk.get("course"),
            "document": chunk.get("document"),
            "page": chunk.get("page"),
            "score": chunk.get("score"),
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
