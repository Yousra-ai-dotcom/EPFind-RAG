"""
Personne 2 — Embeddings + Search
Rôle : transformer les chunks de texte en vecteurs (embeddings) via Azure OpenAI.

(Complété ici pour débloquer la démo.)
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY:
            raise ValueError("AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_KEY manquants dans .env")
        _client = OpenAI(
            api_key=AZURE_OPENAI_KEY,
            base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/",
        )
    return _client


def get_embedding(text: str) -> list[float]:
    """Appelle le déploiement d'embedding Azure OpenAI et retourne le vecteur."""
    if not AZURE_OPENAI_EMBEDDING_DEPLOYMENT:
        raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT manquant dans .env")

    client = _get_client()
    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
    )
    return response.data[0].embedding


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Version batch : envoie plusieurs textes en une seule requête (indexation)."""
    if not AZURE_OPENAI_EMBEDDING_DEPLOYMENT:
        raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT manquant dans .env")

    client = _get_client()
    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=texts,
    )
    return [item.embedding for item in response.data]
