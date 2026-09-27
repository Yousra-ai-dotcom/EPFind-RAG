"""
Tests for EPFind FastAPI backend.

External Azure services are mocked.
No real Blob Storage or Azure AI Search resource is modified.
"""

from types import SimpleNamespace
from unittest.mock import ANY, patch
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
@patch("backend.routes.ask.answer_question")
@patch("backend.routes.ask.add_message")
@patch("backend.routes.ask.create_conversation")
@patch("backend.routes.ask.get_or_create_user")
def test_ask_creates_conversation_for_current_user(
    mock_get_or_create_user,
    mock_create_conversation,
    mock_add_message,
    mock_answer_question,
):
    fake_user = SimpleNamespace(id=42)

    fake_conversation = SimpleNamespace(
        id=100,
        user_id=42,
    )

    mock_get_or_create_user.return_value = fake_user
    mock_create_conversation.return_value = fake_conversation

    mock_answer_question.return_value = {
        "answer": "Git est un systÃ¨me de gestion de versions.",
        "sources": [],

    }

    from backend.auth.entra import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {
        "name": "Test User",
        "email": "test@epf.fr",
        "microsoft_id": "microsoft-test-id",

    }

    try:
        response = client.post(
            "/ask",
            json={
                "question": "Qu'est-ce que Git ?",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["conversation_id"] == 100
        assert data["answer"] == (
            "Git est un systÃ¨me de gestion de versions."
        )

        mock_create_conversation.assert_called_once_with(
            db=ANY,
            title="Qu'est-ce que Git ?",
            user_id=42,
        )

    finally:
        app.dependency_overrides.clear()

@patch("backend.routes.history.get_conversations")
@patch("backend.routes.history.get_or_create_user")
def test_history_returns_current_user_conversations(
    mock_get_or_create_user,
    mock_get_conversations,
):
    fake_user = SimpleNamespace(id=42)

    fake_conversation = SimpleNamespace(
        id=100,
        title="Question sur Git",
        created_at="2026-09-27T12:00:00",
    )

    mock_get_or_create_user.return_value = fake_user
    mock_get_conversations.return_value = [fake_conversation]

    from backend.auth.entra import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {
        "name": "Test User",
        "email": "test@epf.fr",
        "microsoft_id": "microsoft-test-id",

    }

    try:
        response = client.get("/history")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data["conversations"][0]["id"] == 100
        assert data["conversations"][0]["title"] == "Question sur Git"

        mock_get_conversations.assert_called_once_with(
            db=ANY,
            user_id=42,
        )

    finally:
        app.dependency_overrides.clear()

@patch("backend.routes.history.get_conversation_by_id")
@patch("backend.routes.history.get_or_create_user")
def test_history_forbids_other_user_conversation(
    mock_get_or_create_user,
    mock_get_conversation_by_id,
):
    # Utilisateur actuellement connectÃ©
    fake_user = SimpleNamespace(id=42)

    # Conversation appartenant Ã  un autre utilisateur
    fake_conversation = SimpleNamespace(
        id=100,
        user_id=99,
        title="Conversation privÃ©e",
        created_at="2026-09-27T12:00:00",
        messages=[],
    )

    mock_get_or_create_user.return_value = fake_user
    mock_get_conversation_by_id.return_value = fake_conversation

    from backend.auth.entra import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {
        "name": "Test User",
        "email": "test@epf.fr",
        "microsoft_id": "microsoft-test-id",

    }

    try:
        response = client.get("/history/100")

        assert response.status_code == 403

        assert response.json() == {
            "detail": "Accès interdit à cette conversation.",
        }
        mock_get_conversation_by_id.assert_called_once_with(
            db=ANY,
            conversation_id=100,
        )

    finally:
        app.dependency_overrides.clear()












