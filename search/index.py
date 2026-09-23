"""
Azure AI Search — création et alimentation de l'index.

Un document dans l'index = un chunk de cours + son embedding.
"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    HnswAlgorithmConfiguration,
    VectorSearch,
    VectorSearchProfile,
)

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "epf-courses-index",
)

if not AZURE_SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT manquant dans .env")

if not AZURE_SEARCH_KEY:
    raise ValueError("AZURE_SEARCH_KEY manquant dans .env")


credential = AzureKeyCredential(AZURE_SEARCH_KEY)


def create_index() -> None:
    """
    Crée ou met à jour l'index Azure AI Search.
    """

    index_client = SearchIndexClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        credential=credential,
    )

    fields = [
        SearchField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),

        SearchField(
            name="course_id",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
        ),

        SearchField(
            name="course_name",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
        ),

        SearchField(
            name="module",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
        ),

        SearchField(
            name="chapter",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
        ),

        SearchField(
            name="page",
            type=SearchFieldDataType.Int32,
            filterable=True,
            sortable=True,
        ),

        SearchField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
            retrievable=True,
        ),

        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(
                SearchFieldDataType.Single
            ),
            searchable=True,
            retrievable=False,
            vector_search_dimensions=1536,
            vector_search_profile_name="vector-profile",
        ),

        SearchField(
            name="document_name",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-config",
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config",
            )
        ],
    )

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
    )

    result = index_client.create_or_update_index(index)

    print(f"Index créé avec succès : {result.name}")


def upload_documents(documents: list[dict]) -> None:
    """
    Envoie des chunks + embeddings dans Azure AI Search.
    """

    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=credential,
    )

    result = search_client.upload_documents(documents=documents)

    success_count = sum(
        1 for item in result if item.succeeded
    )

    print(
        f"{success_count}/{len(documents)} documents "
        f"envoyés avec succès."
    )


if __name__ == "__main__":
    create_index()
