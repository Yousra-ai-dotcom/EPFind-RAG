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