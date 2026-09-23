"""
Personne 3 — Prompt + LLM

Rôle : gérer la connexion à Azure OpenAI (chat completions).
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_CHAT_DEPLOYMENT"
)

if not AZURE_OPENAI_ENDPOINT:
    raise ValueError("AZURE_OPENAI_ENDPOINT manquant dans .env")

if not AZURE_OPENAI_KEY:
    raise ValueError("AZURE_OPENAI_KEY manquant dans .env")

if not AZURE_OPENAI_CHAT_DEPLOYMENT:
    raise ValueError(
        "AZURE_OPENAI_CHAT_DEPLOYMENT manquant dans .env"
    )

client = OpenAI(
    api_key=AZURE_OPENAI_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/",
)


def call_llm(prompt: str, temperature: float = 0.3) -> str:
    """
    Envoie un prompt à Azure OpenAI et retourne la réponse générée.
    """

    response = client.chat.completions.create(
        model=AZURE_OPENAI_CHAT_DEPLOYMENT,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content
