"""
Personne 2 — Embeddings + Search
Rôle : rechercher les chunks les plus pertinents pour une question donnée,
avec filtrage optionnel par cours.

Utilisé ensuite par `generation/answer.py` (Personne 3) et par le backend.

(Complété ici pour débloquer la démo — Yousra doit relire/adapter selon
la structure exacte de son index Azure AI Search.)
"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from search.embeddings import get_embedding

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "epf-courses-index")

_client: SearchClient | None = None


def _get_client() -> SearchClient:
    global _client
    if _client is None:
        if not SEARCH_ENDPOINT or not SEARCH_KEY:
            raise ValueError(
                "AZURE_SEARCH_ENDPOINT / AZURE_SEARCH_KEY manquants dans .env"
            )
        _client = SearchClient(
            endpoint=SEARCH_ENDPOINT,
            index_name=SEARCH_INDEX,
            credential=AzureKeyCredential(SEARCH_KEY),
        )
    return _client


def retrieve(question: str, course: str | None = None, top_k: int = 5) -> list[dict]:
    """
    1. Calcule l'embedding de la question.
    2. Interroge Azure AI Search en mode hybride (texte + vecteur).
    3. Filtre sur course_name si un cours est précisé.
    4. Retourne les top_k chunks les plus pertinents.
    """
    client = _get_client()
    question_vector = get_embedding(question)

    vector_query = VectorizedQuery(
        vector=question_vector,
        k_nearest_neighbors=top_k,
        fields="content_vector",
    )

    filter_expr = None
    if course:
        # échappe les apostrophes pour éviter de casser le filtre OData
        safe_course = course.replace("'", "''")
        filter_expr = f"course_name eq '{safe_course}'"

    results = client.search(
        search_text=question,          # recherche texte (keyword)
        vector_queries=[vector_query], # recherche vectorielle (sens)
        filter=filter_expr,
        top=top_k,
        select=["course_name", "module", "chapter", "page", "content", "document_name"],
    )

    chunks = []
    for r in results:
        chunks.append({
            "course": r.get("course_name"),
            "module": r.get("module"),
            "chapter": r.get("chapter"),
            "page": r.get("page"),
            "text": r.get("content"),
            "document_name": r.get("document_name"),
        })

    return chunks


def retrieve_full_course(course: str, max_chunks: int = 40) -> list[dict]:
    """
    Récupère un large échantillon de chunks d'un cours donné, utilisé
    pour la révision (résumé) et la génération de QCM, qui ont besoin
    de plus de contexte qu'une simple question.
    """
    client = _get_client()
    safe_course = course.replace("'", "''")

    results = client.search(
        search_text="*",
        filter=f"course_name eq '{safe_course}'",
        top=max_chunks,
        select=["course_name", "module", "chapter", "page", "content", "document_name"],
    )

    chunks = []
    for r in results:
        chunks.append({
            "course": r.get("course_name"),
            "module": r.get("module"),
            "chapter": r.get("chapter"),
            "page": r.get("page"),
            "text": r.get("content"),
            "document_name": r.get("document_name"),
        })

    return chunks
