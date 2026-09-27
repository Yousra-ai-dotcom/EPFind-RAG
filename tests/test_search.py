"""
Tests — Search / Embeddings

Tests unitaires de la génération d'embeddings
et de la recherche de documents.
Les appels Azure sont simulés avec des mocks.
"""

from unittest.mock import MagicMock, patch

from search.embeddings import generate_embedding
from search.retrieval import retrieve


@patch("search.embeddings.client")
def test_generate_embedding(mock_client):
    """Vérifie que generate_embedding retourne correctement un vecteur."""

    fake_embedding = [0.1, 0.2, 0.3]

    mock_response = MagicMock()
    mock_response.data = [
        MagicMock(embedding=fake_embedding)
    ]

    mock_client.embeddings.create.return_value = mock_response

    result = generate_embedding("Test EPFind")

    assert result == fake_embedding
    mock_client.embeddings.create.assert_called_once()


@patch("search.retrieval.search_client")
@patch("search.retrieval.generate_embedding")
def test_retrieve(mock_generate_embedding, mock_search_client):
    """Vérifie que retrieve retourne les documents trouvés."""

    mock_generate_embedding.return_value = [0.1] * 1536

    fake_result = {
        "id": "test-id",
        "content": "Git permet de gérer les versions d'un projet.",
        "module": "GIT",
        "course": "Introduction",
        "page": 1,
        "document": "introduction.pdf",
        "@search.score": 0.95,
    }

    mock_search_client.search.return_value = [fake_result]

    results = retrieve(
        question="Qu'est-ce que Git ?",
        module="GIT",
        top_k=3,
    )

    assert len(results) == 1

    assert results[0]["content"] == (
        "Git permet de gérer les versions d'un projet."
    )

    assert results[0]["module"] == "GIT"
    assert results[0]["course"] == "Introduction"
    assert results[0]["page"] == 1
    assert results[0]["document"] == "introduction.pdf"

    mock_generate_embedding.assert_called_once_with(
        "Qu'est-ce que Git ?"
    )

    mock_search_client.search.assert_called_once()

@patch("search.retrieval.get_search_client")
def test_course_is_indexed(mock_get_search_client):
    """Vérifie qu'un cours présent dans Azure Search est détecté."""

    mock_client = MagicMock()
    mock_get_search_client.return_value = mock_client

    mock_client.search.return_value = [
        {"id": "chunk-1"}
    ]

    from search.retrieval import course_is_indexed

    result = course_is_indexed(
        module="GIT",
        course="Introduction",
    )

    assert result is True

    mock_client.search.assert_called_once()

    call_kwargs = mock_client.search.call_args.kwargs

    assert (
        call_kwargs["filter"]
        == "module eq 'GIT' and course eq 'Introduction'"
    )

    assert call_kwargs["select"] == ["id"]
    assert call_kwargs["top"] == 1


@patch("search.retrieval.get_search_client")
def test_delete_indexed_course(mock_get_search_client):
    """Vérifie la suppression de tous les chunks d'un cours."""

    mock_client = MagicMock()
    mock_get_search_client.return_value = mock_client

    mock_client.search.return_value = [
        {"id": "chunk-1"},
        {"id": "chunk-2"},
        {"id": "chunk-3"},
    ]

    mock_client.delete_documents.return_value = [
        MagicMock(succeeded=True),
        MagicMock(succeeded=True),
        MagicMock(succeeded=True),
    ]

    from search.retrieval import delete_indexed_course

    deleted = delete_indexed_course(
        module="GIT",
        course="Introduction",
    )

    assert deleted == 3

    mock_client.search.assert_called_once()

    search_kwargs = mock_client.search.call_args.kwargs

    assert (
        search_kwargs["filter"]
        == "module eq 'GIT' and course eq 'Introduction'"
    )

    assert search_kwargs["select"] == ["id"]

    mock_client.delete_documents.assert_called_once_with(
        documents=[
            {"id": "chunk-1"},
            {"id": "chunk-2"},
            {"id": "chunk-3"},
        ]
    )