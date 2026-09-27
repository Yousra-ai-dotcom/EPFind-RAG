"""
Tests for EPFind FastAPI backend.

External Azure services are mocked.
No real Blob Storage or Azure AI Search resource is modified.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


@patch("backend.routes.documents.list_courses")
def test_get_documents(mock_list_courses):
    mock_list_courses.return_value = [
        {
            "blob_name": "GIT/Introduction.pdf",
            "module": "GIT",
            "course": "Introduction",
            "document": "Introduction.pdf",
        }
    ]

    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["module"] == "GIT"
    assert data[0]["course"] == "Introduction"

    mock_list_courses.assert_called_once()


@patch("backend.routes.documents.upload_and_process_course")
def test_upload_document(mock_upload_and_process):
    mock_upload_and_process.return_value = {
        "blob_name": "GIT/Introduction.pdf",
        "module": "GIT",
        "course": "Introduction",
        "document": "Introduction.pdf",
        "chunks": 10,
        "indexed_chunks": 10,
        "indexed": True,
    }

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "Introduction.pdf",
                b"%PDF-1.4 fake pdf",
                "application/pdf",
            )
        },
        data={
            "module": "GIT",
            "course": "Introduction",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["blob_name"] == "GIT/Introduction.pdf"
    assert data["indexed"] is True
    assert data["chunks"] == 10

    mock_upload_and_process.assert_called_once()

    call_kwargs = mock_upload_and_process.call_args.kwargs

    assert call_kwargs["module"] == "GIT"
    assert call_kwargs["course"] == "Introduction"


@patch(
    "backend.routes.documents.delete_indexed_course",
    return_value=10,
)
@patch(
    "backend.routes.documents.delete_course",
    return_value=True,
)
def test_delete_document(
    mock_delete_course,
    mock_delete_indexed_course,
):
    response = client.delete(
        "/documents/GIT/Introduction.pdf"
    )

    assert response.status_code == 200

    assert response.json() == {
        "deleted": True,
        "blob_name": "GIT/Introduction.pdf",
        "deleted_chunks": 10,
    }

    mock_delete_course.assert_called_once_with(
        "GIT/Introduction.pdf"
    )

    mock_delete_indexed_course.assert_called_once_with(
        module="GIT",
        course="Introduction",
    )


@patch(
    "backend.routes.documents.delete_course",
    return_value=False,
)
def test_delete_document_not_found(mock_delete_course):
    response = client.delete(
        "/documents/GIT/Unknown.pdf"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Document introuvable.",
    }

    mock_delete_course.assert_called_once_with(
        "GIT/Unknown.pdf"
    )