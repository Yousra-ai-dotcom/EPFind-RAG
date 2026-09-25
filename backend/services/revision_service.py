"""
Service de révision d'EPFind.

Ce service récupère le contenu d'un cours depuis Azure AI Search
puis utilise le LLM pour générer le type de révision demandé.
"""

from search.retrieval import get_course_content
from generation.prompts import SUMMARY_PROMPT
from generation.llm import call_llm


SUMMARY_INSTRUCTIONS = {
    "resume_rapide": (
        "Fais un résumé court et synthétique du cours, "
        "avec uniquement les notions essentielles."
    ),
    "resume_detaille": (
        "Fais un résumé détaillé et structuré du cours, "
        "en expliquant les notions importantes."
    ),
    "points_cles": (
        "Présente uniquement les points clés du cours "
        "sous forme de liste claire."
    ),
    "fiche_de_revision": (
        "Crée une fiche de révision structurée avec les notions importantes, "
        "définitions, concepts, exemples et points à retenir."
    ),
    "explication_pedagogique": (
        "Explique le contenu du cours de manière simple, progressive "
        "et pédagogique pour aider un étudiant à le comprendre."
    ),
}


def generate_course_summary(
    course: str,
    summary_type: str = "resume_rapide",
) -> str:
    """
    Génère une révision à partir du contenu d'un cours indexé.
    """

    if not course or not course.strip():
        raise ValueError("Le cours doit être précisé.")

    if summary_type not in SUMMARY_INSTRUCTIONS:
        raise ValueError(
            "Type de résumé invalide. "
            "Valeurs possibles : "
            + ", ".join(SUMMARY_INSTRUCTIONS.keys())
        )

    # Récupération du contenu depuis Azure AI Search
    chunks = get_course_content(
        course=course,
        max_chunks=50,
    )

    if not chunks:
        raise ValueError(
            f"Aucun contenu trouvé pour le cours '{course}'."
        )

    course_content = "\n\n".join(
        chunk["content"]
        for chunk in chunks
        if chunk.get("content")
    )

    if not course_content.strip():
        raise ValueError(
            f"Le cours '{course}' ne contient aucun texte exploitable."
        )

    # Prompt existant créé par la partie génération
    prompt = SUMMARY_PROMPT.format(
        course=course,
        context=course_content,
    )

    # Ajout du format demandé par le frontend
    prompt += (
        "\n\nConsigne de format :\n"
        + SUMMARY_INSTRUCTIONS[summary_type]
    )

    return call_llm(
    prompt=prompt,
    max_completion_tokens=4000,
)