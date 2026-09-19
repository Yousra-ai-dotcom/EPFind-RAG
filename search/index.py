"""
Personne 2 — Embeddings + Search
Rôle : créer et alimenter l'index Azure AI Search.

Schéma d'index cible (un document = un chunk) :
{
    "id": "chunk-uuid",
    "course_id": "ml-01",
    "course_name": "Machine Learning",
    "module": "Artificial Intelligence",
    "chapter": "Classification",
    "page": 25,
    "content": "La classification supervisée...",
    "content_vector": [...],
    "document_name": "cours-01.pdf"
}
"""

import os
from dotenv import load_dotenv

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "epf-courses-index")


def create_index() -> None:
    """
    TODO (Personne 2) :
    - Créer l'index Azure AI Search avec les champs ci-dessus
    - Configurer le champ content_vector comme champ vectoriel
    """
    raise NotImplementedError


def upload_documents(chunks_with_embeddings: list[dict]) -> None:
    """
    TODO (Personne 2) :
    - Envoyer les chunks (avec leur vecteur) dans l'index Azure AI Search
    """
    raise NotImplementedError
