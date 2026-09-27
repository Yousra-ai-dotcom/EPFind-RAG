"""
Tests for the EPFind ingestion pipeline.

The PDF loader and ingestion components are mocked so that
the tests do not depend on an external PDF file.
"""

from unittest.mock import patch

from ingestion.pipeline import process_pdf


@patch("ingestion.pipeline.attach_metadata")
@patch("ingestion.pipeline.chunk_text")
@patch("ingestion.pipeline.clean_text")
@patch("ingestion.pipeline.load_pdf")
def test_process_pdf(
    mock_load_pdf,
    mock_clean_text,
    mock_chunk_text,
    mock_attach_metadata,
):
    """Vérifie le pipeline PDF -> nettoyage -> chunks -> métadonnées."""

    mock_load_pdf.return_value = [
        {
            "page": 1,
            "text": " Texte de cours EPFind ",
        }
    ]

    mock_clean_text.return_value = "Texte de cours EPFind"

    mock_chunk_text.return_value = [
        "Premier chunk",
        "Deuxième chunk",
    ]

    mock_attach_metadata.side_effect = [
        {
            "text": "Premier chunk",
            "page": 1,
            "document": "cours.pdf",
        },
        {
            "text": "Deuxième chunk",
            "page": 1,
            "document": "cours.pdf",
        },
    ]

    result = process_pdf("/tmp/cours.pdf")

    assert len(result) == 2

    assert result[0] == {
        "text": "Premier chunk",
        "page": 1,
        "document": "cours.pdf",
    }

    assert result[1] == {
        "text": "Deuxième chunk",
        "page": 1,
        "document": "cours.pdf",
    }

    mock_load_pdf.assert_called_once_with("/tmp/cours.pdf")

    mock_clean_text.assert_called_once_with(
        " Texte de cours EPFind "
    )

    mock_chunk_text.assert_called_once_with(
        "Texte de cours EPFind"
    )

    assert mock_attach_metadata.call_count == 2


@patch("ingestion.pipeline.chunk_text")
@patch("ingestion.pipeline.clean_text")
@patch("ingestion.pipeline.load_pdf")
def test_process_pdf_ignores_empty_pages(
    mock_load_pdf,
    mock_clean_text,
    mock_chunk_text,
):
    """Vérifie qu'une page vide après nettoyage est ignorée."""

    mock_load_pdf.return_value = [
        {
            "page": 1,
            "text": "   ",
        }
    ]

    mock_clean_text.return_value = ""

    result = process_pdf("/tmp/empty.pdf")

    assert result == []

    mock_clean_text.assert_called_once_with("   ")

    mock_chunk_text.assert_not_called()