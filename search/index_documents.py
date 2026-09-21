import os
import uuid

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from embeddings import generate_embedding


load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "epfind-courses")


search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def index_documents(chunks: list[dict]):
    """
    Génère l'embedding de chaque chunk puis l'envoie
    dans Azure AI Search.
    """

    documents = []

    for chunk in chunks:

        content = chunk["content"]

        # Générer l'embedding du texte
        embedding = generate_embedding(content)

        document = {
            "id": str(uuid.uuid4()),
            "content": content,
            "course": chunk.get("course", ""),
            "chapter": chunk.get("chapter", ""),
            "page": chunk.get("page", 0),
            "document": chunk.get("document", ""),
            "content_vector": embedding,
        }

        documents.append(document)

    result = search_client.upload_documents(documents=documents)

    successful = sum(1 for r in result if r.succeeded)

    print(f"{successful}/{len(documents)} chunks indexés avec succès.")

    return result


if __name__ == "__main__":

    # Données temporaires uniquement pour tester notre pipeline
    test_chunks = [
        {
            "content": (
                "Le prompt injection est une attaque dans laquelle "
                "un utilisateur fournit des instructions malveillantes "
                "afin de modifier le comportement d'un modèle de langage."
            ),
            "course": "Chatbot",
            "chapter": "Sécurité",
            "page": 10,
            "document": "cours-chatbot-test.pdf",
        },
        {
            "content": (
                "Le RAG combine la recherche d'informations dans une "
                "base documentaire avec la génération de réponses par un LLM."
            ),
            "course": "Chatbot",
            "chapter": "RAG",
            "page": 20,
            "document": "cours-chatbot-test.pdf",
        },
        {
            "content": (
                "Les embeddings représentent les textes sous forme de "
                "vecteurs afin de permettre une recherche par similarité."
            ),
            "course": "Chatbot",
            "chapter": "Embeddings",
            "page": 21,
            "document": "cours-chatbot-test.pdf",
        },
    ]

    index_documents(test_chunks)