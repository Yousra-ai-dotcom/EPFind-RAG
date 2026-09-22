"""
Prompt + LLM
Rôle : gérer la connexion à Azure OpenAI (chat completions).
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def call_llm(prompt: str, temperature: float = 0.3) -> str:
    """
    Envoie un prompt à Azure OpenAI et retourne la réponse du modèle.

    Le paramètre temperature est conservé dans la signature
    pour rester compatible avec le reste du projet, mais il
    n'est pas envoyé à GPT-5-mini.
    """

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT est manquant.")

    if not api_key:
        raise ValueError("AZURE_OPENAI_KEY est manquant.")

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
        max_completion_tokens=800,
    )

    return response.choices[0].message.content