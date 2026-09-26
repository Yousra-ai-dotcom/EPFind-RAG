"""
Prompt + LLM
Rôle : gérer la connexion à Azure OpenAI (chat completions).
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def call_llm(
    prompt: str,
    temperature: float = 0.3,
    max_completion_tokens: int = 1200,
) -> str:
    """
    Envoie un prompt à Azure OpenAI (déploiement GPT-5-mini) et retourne
    le texte de la réponse du modèle.
    """

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT est manquant.")
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY est manquant.")
    if not deployment:
        raise ValueError("AZURE_OPENAI_CHAT_DEPLOYMENT est manquant.")

    client = OpenAI(
        api_key=api_key,
        base_url=f"{endpoint.rstrip('/')}/openai/v1/",
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=max_completion_tokens,
    )

    return response.choices[0].message.content
