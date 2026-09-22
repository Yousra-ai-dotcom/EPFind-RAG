"""
Azure Blob Storage service for EPFind.

This module manages course PDF files stored in Azure Blob Storage.
"""

from pathlib import Path
from typing import Optional


def upload_course(
    file_path: str,
    module: str,
    course: str,
) -> dict:
    """
    Upload a course PDF to Azure Blob Storage.

    Args:
        file_path: Local path of the PDF.
        module: Course module, e.g. "GIT".
        course: Course name, e.g. "Les commits".

    Returns:
        Information about the uploaded document.
    """
    pass


def list_courses() -> list[dict]:
    """
    Return all course documents stored in Azure Blob Storage.
    """
    pass


def download_course(
    blob_name: str,
    destination_path: Optional[str] = None,
) -> str:
    """
    Download a course PDF from Azure Blob Storage.

    Returns:
        Local path of the downloaded PDF.
    """
    pass


def delete_course(blob_name: str) -> bool:
    """
    Delete a course PDF from Azure Blob Storage.
    """
    pass


def course_exists(blob_name: str) -> bool:
    """
    Check whether a document already exists in Azure Blob Storage.
    """
    pass


def validate_pdf(file_path: str) -> bool:
    """
    Validate that the uploaded document is a PDF.
    """
    pass