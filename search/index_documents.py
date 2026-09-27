import hashlib
import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from search.embeddings import generate_embedding

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "epfind-courses",
)

search_client = None


def get_search_client():
    """
    Initialise le client Azure AI Search uniquement lorsqu'il est nécessaire.
    """
    global search_client

    if search_client is None:
        if not AZURE_SEARCH_ENDPOINT:
            raise ValueError(
                "AZURE_SEARCH_ENDPOINT est manquant."
            )

        if not AZURE_SEARCH_API_KEY:
            raise ValueError(
                "AZURE_SEARCH_API_KEY est manquant."
            )

        search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=INDEX_NAME,
            credential=AzureKeyCredential(
                AZURE_SEARCH_API_KEY
            ),
        )

    return search_client


def generate_document_id(
    chunk: dict,
    content: str,
) -> str:
    source = "|".join([
        chunk.get("module", ""),
        chunk.get("course", ""),
        chunk.get("document", ""),
        str(chunk.get("page", 0)),
        content,
    ])

    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()


def index_documents(chunks: list[dict]):
    """
    Reçoit les chunks produits par l'ingestion,
    génère leurs embeddings et les indexe dans Azure AI Search.
    """
    documents = []

    for chunk in chunks:
        content = chunk.get("text", "")

        if not content.strip():
            continue

        embedding = generate_embedding(content)

        document = {
            "id": generate_document_id(
                chunk,
                content,
            ),
            "content": content,
            "module": chunk.get("module", ""),
            "course": chunk.get("course", ""),
            "page": chunk.get("page", 0),
            "document": chunk.get("document", ""),
            "content_vector": embedding,
        }

        documents.append(document)

    if not documents:
        print("Aucun chunk à indexer.")
        return []

    result = get_search_client().upload_documents(
        documents=documents
    )

    successful = sum(
        1 for item in result
        if item.succeeded
    )

    print(
        f"{successful}/{len(documents)} "
        "chunks indexés avec succès."
    )

    return result