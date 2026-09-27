"""
Tests for EPFind course storage.

Azure services are mocked: these tests do not modify
the real EPFind Azure resources.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from storage.blob_service import (
    course_exists,
    delete_course,
    list_courses,
    upload_course,
    validate_pdf,
)
from storage.course_manager import upload_and_process_course


def test_pdf_validation(tmp_path):
    pdf = tmp_path / "cours.pdf"
    pdf.write_bytes(b"%PDF-1.4 test")

    txt = tmp_path / "cours.txt"
    txt.write_text("test")

    assert validate_pdf(str(pdf)) is True
    assert validate_pdf(str(txt)) is False
    assert validate_pdf(str(tmp_path / "missing.pdf")) is False


@patch("storage.blob_service._get_container_client")
def test_course_upload(mock_get_container, tmp_path):
    pdf = tmp_path / "original.pdf"
    pdf.write_bytes(b"%PDF-1.4 test")

    container = MagicMock()
    blob_client = MagicMock()
    container.get_blob_client.return_value = blob_client
    mock_get_container.return_value = container

    result = upload_course(
        file_path=str(pdf),
        module="Reseaux",
        course="RT0",
    )

    assert result == {
        "blob_name": "Reseaux/RT0.pdf",
        "module": "Reseaux",
        "course": "RT0",
        "document": "RT0.pdf",
    }

    container.get_blob_client.assert_called_once_with(
        "Reseaux/RT0.pdf"
    )

    blob_client.upload_blob.assert_called_once()
    assert blob_client.upload_blob.call_args.kwargs["overwrite"] is True


@patch("storage.blob_service._get_container_client")
def test_course_listing(mock_get_container):
    container = MagicMock()
    container.list_blobs.return_value = [
        SimpleNamespace(name="GIT/Introduction.pdf"),
        SimpleNamespace(name="GIT/Branches.pdf"),
        SimpleNamespace(name="GIT/readme.txt"),
    ]

    mock_get_container.return_value = container

    courses = list_courses()

    assert len(courses) == 2

    assert courses[0] == {
        "blob_name": "GIT/Introduction.pdf",
        "module": "GIT",
        "course": "Introduction",
        "document": "Introduction.pdf",
    }

    assert courses[1]["course"] == "Branches"


@patch("storage.blob_service._get_container_client")
def test_course_exists(mock_get_container):
    container = MagicMock()
    blob_client = MagicMock()

    blob_client.exists.return_value = True
    container.get_blob_client.return_value = blob_client
    mock_get_container.return_value = container

    assert course_exists("GIT/Introduction.pdf") is True

    container.get_blob_client.assert_called_once_with(
        "GIT/Introduction.pdf"
    )


@patch("storage.blob_service._get_container_client")
def test_course_delete(mock_get_container):
    container = MagicMock()
    blob_client = MagicMock()

    blob_client.exists.return_value = True
    container.get_blob_client.return_value = blob_client
    mock_get_container.return_value = container

    deleted = delete_course("GIT/Introduction.pdf")

    assert deleted is True
    blob_client.delete_blob.assert_called_once()


@patch("storage.course_manager.process_course")
@patch("storage.course_manager.upload_course")
def test_course_processing(
    mock_upload_course,
    mock_process_course,
):
    mock_upload_course.return_value = {
        "blob_name": "GIT/Introduction.pdf",
        "module": "GIT",
        "course": "Introduction",
        "document": "Introduction.pdf",
    }

    mock_process_course.return_value = {
        "module": "GIT",
        "course": "Introduction",
        "chunks": 10,
        "indexed_chunks": 10,
        "indexed": True,
        "blob_name": "GIT/Introduction.pdf",
    }

    result = upload_and_process_course(
        file_path="/tmp/Introduction.pdf",
        module="GIT",
        course="Introduction",
    )

    assert result["blob_name"] == "GIT/Introduction.pdf"
    assert result["indexed"] is True
    assert result["chunks"] == 10
    assert result["indexed_chunks"] == 10

    mock_upload_course.assert_called_once_with(
        file_path="/tmp/Introduction.pdf",
        module="GIT",
        course="Introduction",
    )

    mock_process_course.assert_called_once_with(
        blob_name="GIT/Introduction.pdf",
        module="GIT",
        course="Introduction",
    )