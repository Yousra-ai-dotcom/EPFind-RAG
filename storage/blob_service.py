"""
Azure Blob Storage service for EPFind.

This module manages course PDF files stored in Azure Blob Storage.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient


load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING"
)

AZURE_STORAGE_CONTAINER = os.getenv(
    "AZURE_STORAGE_CONTAINER",
    "cours-epf",
)


def _get_container_client():
    """
    Return the Azure Blob Storage container client.
    """

    if not AZURE_STORAGE_CONNECTION_STRING:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING est manquant dans .env"
        )

    service = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )

    return service.get_container_client(
        AZURE_STORAGE_CONTAINER
    )


def validate_pdf(file_path: str) -> bool:
    """
    Check that the local file exists and is a PDF.
    """

    path = Path(file_path)

    return (
        path.exists()
        and path.is_file()
        and path.suffix.lower() == ".pdf"
    )


def upload_course(
    file_path: str,
    module: str,
    course: str,
) -> dict:
    """
    Upload a course PDF to Azure Blob Storage.

    The document is stored as:
    <module>/<filename>
    """

    if not module or not module.strip():
        raise ValueError("Le module ne peut pas être vide.")

    if not course or not course.strip():
        raise ValueError("Le nom du cours ne peut pas être vide.")

    if not validate_pdf(file_path):
        raise ValueError(
            "Le fichier doit être un PDF valide."
        )

    container = _get_container_client()

    path = Path(file_path)

    blob_name = f"{module.strip()}/{path.name}"

    blob_client = container.get_blob_client(
        blob_name
    )

    with open(path, "rb") as file:
        blob_client.upload_blob(
            file,
            overwrite=True,
        )

    return {
        "blob_name": blob_name,
        "module": module.strip(),
        "course": course.strip(),
        "document": path.name,
    }


def list_courses() -> list[dict]:
    """
    Return all PDF course documents stored in Azure Blob Storage.
    """

    container = _get_container_client()

    courses = []

    for blob in container.list_blobs():

        if not blob.name.lower().endswith(".pdf"):
            continue

        parts = blob.name.split("/")

        module = (
            parts[0]
            if len(parts) > 1
            else "General"
        )

        filename = parts[-1]

        courses.append(
            {
                "blob_name": blob.name,
                "module": module,
                "course": Path(filename).stem,
                "document": filename,
            }
        )

    return courses


def download_course(
    blob_name: str,
    destination_path: Optional[str] = None,
) -> str:
    """
    Download a course PDF from Azure Blob Storage.

    Returns:
        Local path of the downloaded PDF.
    """

    container = _get_container_client()

    blob_client = container.get_blob_client(
        blob_name
    )

    if destination_path is None:

        temp_directory = tempfile.mkdtemp(
            prefix="epfind_"
        )

        destination_path = str(
            Path(temp_directory) / Path(blob_name).name
        )

    destination = Path(destination_path)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(destination, "wb") as file:
        data = blob_client.download_blob()
        file.write(data.readall())

    return str(destination)


def delete_course(blob_name: str) -> bool:
    """
    Delete a course PDF from Azure Blob Storage.
    """
    raise NotImplementedError


def course_exists(blob_name: str) -> bool:
    """
    Check whether a document already exists in Azure Blob Storage.
    """
    raise NotImplementedError