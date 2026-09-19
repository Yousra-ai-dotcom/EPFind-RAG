"""
Personne 2 — Embeddings + Search
Rôle : transformer les chunks de texte en vecteurs (embeddings) via Azure OpenAI.
"""

import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")


def get_embedding(text: str) -> list[float]:
    """
    TODO (Personne 2) :
    - Appeler le déploiement d'embedding Azure OpenAI (text-embedding-3-small/large)
    - Retourner le vecteur (list[float]) correspondant à `text`
    """
    raise NotImplementedError


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    TODO (Personne 2) :
    - Version batch de get_embedding pour indexer tous les chunks efficacement
    """
    raise NotImplementedError
