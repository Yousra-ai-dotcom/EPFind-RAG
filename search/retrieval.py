import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from embeddings import generate_embedding


load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "epfind-courses")


if not AZURE_SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT est manquant dans .env")

if not AZURE_SEARCH_API_KEY:
    raise ValueError("AZURE_SEARCH_API_KEY est manquant dans .env")


search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def retrieve(question: str, top_k: int = 5, course: str | None = None):
    """
    Recherche les chunks de cours les plus pertinents
    dans Azure AI Search.
    """

    if not question or not question.strip():
        raise ValueError("La question ne peut pas être vide.")

    # 1. Transformer la question en embedding
    question_embedding = generate_embedding(question)

    # 2. Recherche vectorielle
    vector_query = VectorizedQuery(
        vector=question_embedding,
        k_nearest_neighbors=top_k,
        fields="content_vector",
    )

    # 3. Filtre facultatif par cours
    filter_expression = None

    if course:
        safe_course = course.replace("'", "''")
        filter_expression = f"course eq '{safe_course}'"

    # 4. Interroger Azure AI Search
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        filter=filter_expression,
        select=[
            "id",
            "content",
            "course",
            "chapter",
            "page",
            "document",
        ],
        top=top_k,
    )

    # 5. Préparer les résultats
    chunks = []

    for result in results:
        chunks.append(
            {
                "id": result.get("id"),
                "content": result.get("content"),
                "course": result.get("course"),
                "chapter": result.get("chapter"),
                "page": result.get("page"),
                "document": result.get("document"),
                "score": result.get("@search.score"),
            }
        )

    return chunks


if __name__ == "__main__":
    question = "Qu'est-ce que le prompt injection ?"

    results = retrieve(question)

    print(f"\nQuestion : {question}")
    print(f"Nombre de résultats : {len(results)}\n")

    for i, result in enumerate(results, start=1):
        print(f"--- Résultat {i} ---")
        print("Cours :", result["course"])
        print("Chapitre :", result["chapter"])
        print("Page :", result["page"])
        print("Document :", result["document"])
        print("Score :", result["score"])
        print("Contenu :", result["content"])
        print()