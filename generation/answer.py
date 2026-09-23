"""
Prompt + LLM
Rôle : assembler question + contexte récupéré en une réponse finale
avec ses sources.
"""

from generation.prompts import QA_PROMPT
from generation.llm import call_llm


def build_answer(question: str, chunks: list[dict]) -> dict:
    if not chunks:
        context = "Aucun contenu trouvé dans les cours."
    else:
        context = "\n\n".join(chunk["text"] for chunk in chunks)

    prompt = QA_PROMPT.format(context=context, question=question)
    answer_text = call_llm(prompt)

    sources = [
        {
           "module": chunk.get("module"),
           "course": chunk.get("course"),
           "document": chunk.get("document"),
           "page": chunk.get("page"),
        }
        for chunk in chunks
    ]

    return {"answer": answer_text, "sources": sources}
