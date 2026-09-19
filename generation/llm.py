"""
Personne 3 — Prompt + LLM
Rôle : gérer la connexion à Azure OpenAI (chat completions).
"""

import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")


def call_llm(prompt: str, temperature: float = 0.3) -> str:
    """
    TODO (Personne 3) :
    - Appeler le endpoint chat completions d'Azure OpenAI avec `prompt`
    - Retourner le texte de la réponse générée
    """
    raise NotImplementedError
