"""
Recherche vectorielle dans Azure AI Search.
"""

import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from search.embeddings import get_embedding


load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "epf-courses-index",
)

if not AZURE_SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT manquant")

if not AZURE_SEARCH_KEY:
    raise ValueError("AZURE_SEARCH_KEY manquant")


search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY),
)


def retrieve(
    question: str,
    course: str | None = None,
    top_k: int = 5,
) -> list[dict]:

    # 1. Embedding de la question
    question_embedding = get_embedding(question)

    # 2. Création de la requête vectorielle
    vector_query = VectorizedQuery(
        vector=question_embedding,
        k_nearest_neighbors=top_k,
        fields="content_vector",
    )

    # 3. Filtre éventuel sur le cours
    filter_expression = None

    if course:
        filter_expression = f"course_name eq '{course}'"

    # 4. Recherche dans Azure AI Search
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        filter=filter_expression,
        select=[
            "id",
            "course_id",
            "course_name",
            "module",
            "chapter",
            "page",
            "content",
            "document_name",
        ],
        top=top_k,
    )

    # 5. Transformation des résultats
    chunks = []

    for result in results:
        chunks.append(
            {
                "id": result["id"],
                "content": result["content"],
                "page": result["page"],
                "document": result["document_name"],
                "course": result["course_name"],
                "score": result["@search.score"],
            }
        )

    return chunks


if __name__ == "__main__":

    question = (
        "Qu'est-ce que l'intelligence artificielle ?"
    )

    print(f"\nQuestion : {question}\n")

    results = retrieve(question)

    print(f"{len(results)} résultats trouvés.\n")

    for i, result in enumerate(results, start=1):

        print("=" * 60)
        print(f"Résultat {i}")
        print(f"Score : {result['score']}")
        print(f"Page : {result['page']}")
        print(f"Document : {result['document']}")
        print()
        print(result["content"][:500])
        print()
