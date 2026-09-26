"""
Service Révision d'EPFind.
Responsable : Personne 3 (génération) — suit le même style que
quiz_service.py et rag_service.py pour rester cohérent avec le reste
du backend (pas de base de données, tout est stateless pour le MVP).
"""

from search.retrieval import get_course_content
from generation.prompts import SUMMARY_PROMPT
from generation.llm import call_llm


ALLOWED_SUMMARY_TYPES = {
    "resume_rapide",
    "resume_detaille",
    "points_cles",
    "fiche_de_revision",
    "explication_pedagogique",
}


def generate_summary(course: str, summary_type: str = "resume_rapide") -> dict:
    """
    Génère une fiche de révision à partir du contenu indexé d'un cours.

    1. Récupère les chunks du cours dans Azure AI Search (get_course_content).
    2. Assemble tout le texte du cours en un seul contexte.
    3. Envoie ce contexte au LLM avec le prompt SUMMARY_PROMPT.
    """

    if not course or not course.strip():
        raise ValueError("Le cours doit être précisé.")

    if summary_type not in ALLOWED_SUMMARY_TYPES:
        raise ValueError(
            f"Type de résumé invalide. Valeurs possibles : {', '.join(ALLOWED_SUMMARY_TYPES)}"
        )

    chunks = get_course_content(course=course, max_chunks=50)

    if not chunks:
        raise ValueError(f"Aucun contenu trouvé pour le cours '{course}'.")

    course_content = "\n\n".join(
        chunk["content"] for chunk in chunks if chunk.get("content")
    )

    if not course_content.strip():
        raise ValueError(f"Le cours '{course}' ne contient aucun texte exploitable.")

    prompt = SUMMARY_PROMPT.format(course=course, context=course_content)
    summary_text = call_llm(prompt, max_completion_tokens=4000)

    return {"summary": summary_text}
