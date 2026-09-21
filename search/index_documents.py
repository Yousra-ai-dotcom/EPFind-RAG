import os
import hashlib
import uuid
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from search.embeddings import generate_embedding
load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "epfind-courses"
)

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)
def generate_document_id(chunk: dict, content: str) -> str:
    source = "|".join([
        chunk.get("module", ""),
        chunk.get("course", ""),
        chunk.get("document", ""),
        str(chunk.get("page", 0)),
        content,
    ])

    return hashlib.sha256(source.encode("utf-8")).hexdigest()

def index_documents(chunks: list[dict]):
    """
    Reçoit les chunks produits par l'ingestion,
    génère leurs embeddings et les indexe dans Azure AI Search.
    """

    documents = []

    for chunk in chunks:

        # Les chunks d'Adam utilisent la clé "text"
        content = chunk.get("text", "")

        if not content.strip():
            continue

        embedding = generate_embedding(content)

        document = {
            "id": generate_document_id(chunk, content),
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

    result = search_client.upload_documents(
        documents=documents
    )

    successful = sum(
        1 for r in result if r.succeeded
    )

    print(
        f"{successful}/{len(documents)} chunks indexés avec succès."
    )

    return result