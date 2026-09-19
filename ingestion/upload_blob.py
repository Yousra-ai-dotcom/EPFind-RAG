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
from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER", "courses")


def upload_pdf(local_path: str, blob_path: str) -> None:
    """
    TODO (Personne 1) :
    - Se connecter à Azure Blob Storage avec azure-storage-blob
    - Uploader `local_path` vers `blob_path` dans AZURE_STORAGE_CONTAINER
    """
    raise NotImplementedError
