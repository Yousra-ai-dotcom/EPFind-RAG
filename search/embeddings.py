import os

from dotenv import load_dotenv
from openai import AzureOpenAI


# Charger les variables du fichier .env
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")


# Vérifier que la configuration existe
if not AZURE_OPENAI_ENDPOINT:
    raise ValueError("AZURE_OPENAI_ENDPOINT est manquant dans .env")

if not AZURE_OPENAI_API_KEY:
    raise ValueError("AZURE_OPENAI_API_KEY est manquant dans .env")

if not EMBEDDING_DEPLOYMENT:
    raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT est manquant dans .env")


# Client Azure OpenAI
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-01",
)


def generate_embedding(text: str) -> list[float]:
    """
    Transforme un texte en vecteur avec Azure OpenAI.
    """

    if not text or not text.strip():
        raise ValueError("Le texte à convertir en embedding est vide.")

    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text,
    )

    return response.data[0].embedding


if __name__ == "__main__":
    test_text = "Le RAG permet à un modèle de rechercher des informations dans des documents."

    embedding = generate_embedding(test_text)

    print("Embedding généré avec succès.")
    print("Nombre de dimensions :", len(embedding))
    print("Premières valeurs :", embedding[:5])
