"""
Service de recherche utilisé par le backend EPFind.

Ce module fait le lien entre le backend FastAPI et
le moteur de recherche vectorielle Azure AI Search.
"""

from search.retrieval import retrieve


def search_course_content(
    question: str,
    module: str | None = None,
    course: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    """
    Recherche les passages de cours les plus pertinents
    pour une question.

    Les résultats de search.retrieval utilisent le champ
    'content'. La couche generation utilise le champ 'text'.
    Ce service adapte donc le format entre les deux couches.
    """

    results = retrieve(
        question=question,
        top_k=top_k,
        module=module,
        course=course,
    )

    chunks = []

    for result in results:
        chunks.append(
            {
                "text": result.get("content", ""),
                "module": result.get("module", ""),
                "course": result.get("course", ""),
                "document": result.get("document", ""),
                "page": result.get("page", 0),
                "score": result.get("score"),
            }
        )

    return chunks