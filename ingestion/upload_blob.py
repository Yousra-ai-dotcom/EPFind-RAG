"""
Personne 1 — Ingestion

Rôle : uploader les PDF des cours vers Azure Blob Storage.

Organisation attendue dans le container :
courses/
  intelligence-artificielle/cours-01.pdf
  chatbot/cours-01.pdf
  big-data/cours-01.pdf
  ...
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient


load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING"
)

AZURE_STORAGE_CONTAINER = os.getenv(
    "AZURE_STORAGE_CONTAINER",
    "courses"
)


def upload_pdf(local_path: str, blob_path: str) -> None:
    """
    Upload un fichier PDF local vers Azure Blob Storage.

    Args:
        local_path: Chemin vers le PDF local.
        blob_path: Chemin souhaité dans Azure Blob Storage.

    Raises:
        ValueError: Si la chaîne de connexion Azure n'est pas configurée.
        FileNotFoundError: Si le fichier local n'existe pas.
    """

    if not AZURE_STORAGE_CONNECTION_STRING:
        raise ValueError(
            "La variable AZURE_STORAGE_CONNECTION_STRING "
            "n'est pas configurée."
        )

    path = Path(local_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {local_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Le chemin indiqué n'est pas un fichier : {local_path}"
        )

    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )

    blob_client = blob_service_client.get_blob_client(
        container=AZURE_STORAGE_CONTAINER,
        blob=blob_path
    )

    with open(path, "rb") as data:
        blob_client.upload_blob(
            data,
            overwrite=True
        )

    print(
        f"Upload réussi : {local_path} "
        f"-> {AZURE_STORAGE_CONTAINER}/{blob_path}"
    )


if __name__ == "__main__":
    # Exemple :
    # upload_pdf(
    #     "../data/courses/cours-01.pdf",
    #     "intelligence-artificielle/cours-01.pdf"
    # )

    print("Module upload_blob.py chargé correctement.")