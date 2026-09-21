import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from search.embeddings import generate_embedding

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "epfind-courses")

if not AZURE_SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT est manquant.")

if not AZURE_SEARCH_API_KEY:
    raise ValueError("AZURE_SEARCH_API_KEY est manquant.")

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def retrieve(
    question: str,
    top_k: int = 5,
    module: str | None = None,
    course: str | None = None,
):
    if not question or not question.strip():
        raise ValueError("La question ne peut pas être vide.")

    question_embedding = generate_embedding(question)

    vector_query = VectorizedQuery(
        vector=question_embedding,
        k_nearest_neighbors=top_k,
        fields="content_vector",
    )

    filters = []

    if module:
        safe_module = module.replace("'", "''")
        filters.append(f"module eq '{safe_module}'")

    if course:
        safe_course = course.replace("'", "''")
        filters.append(f"course eq '{safe_course}'")

    filter_expression = " and ".join(filters) if filters else None

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        filter=filter_expression,
        select=[
            "id",
            "content",
            "module",
            "course",
            "page",
            "document",
        ],
        top=top_k,
    )

    chunks = []

    for result in results:
        chunks.append({
            "id": result.get("id"),
            "content": result.get("content"),
            "module": result.get("module"),
            "course": result.get("course"),
            "page": result.get("page"),
            "document": result.get("document"),
            "score": result.get("@search.score"),
        })

    return chunks