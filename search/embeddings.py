"""
Personne 2 — Embeddings + Search
Rôle : transformer les chunks de texte en vecteurs (embeddings) via Azure OpenAI.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
)

if not AZURE_OPENAI_ENDPOINT:
    raise ValueError("AZURE_OPENAI_ENDPOINT manquant dans .env")

if not AZURE_OPENAI_KEY:
    raise ValueError("AZURE_OPENAI_KEY manquant dans .env")

if not AZURE_OPENAI_EMBEDDING_DEPLOYMENT:
    raise ValueError(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT manquant dans .env"
    )


client = OpenAI(
    api_key=AZURE_OPENAI_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/",
)


def get_embedding(text: str) -> list[float]:
    """
    Transforme un texte en vecteur d'embedding.
    """

    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
    )

    return response.data[0].embedding


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Transforme plusieurs textes en embeddings en une seule requête.
    """

    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=texts,
    )

    return [item.embedding for item in response.data]


if __name__ == "__main__":
    vector = get_embedding(
        "L'intelligence artificielle permet aux machines d'apprendre."
    )

    print("Embedding généré avec succès !")
    print("Dimension :", len(vector))
    print("Premières valeurs :", vector[:5])
