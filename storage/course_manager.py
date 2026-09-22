"""
Course management pipeline for EPFind.

Pipeline:

Azure Blob Storage
        ↓
Download PDF
        ↓
EPFind ingestion
        ↓
Chunks + metadata
        ↓
Azure AI Search indexing
"""

from typing import Optional


def prepare_course_chunks(
    pdf_path: str,
    module: str,
    course: str,
) -> list[dict]:
    """
    Process a PDF using the existing ingestion pipeline
    and add the required EPFind metadata to every chunk.
    """
    pass


def index_course(
    pdf_path: str,
    module: str,
    course: str,
) -> dict:
    """
    Process and index a course into Azure AI Search.
    """
    pass


def process_course(
    blob_name: str,
    module: str,
    course: str,
) -> dict:
    """
    Complete processing pipeline.

    Blob Storage
        -> download
        -> ingestion
        -> metadata
        -> Azure AI Search
    """
    pass


def upload_and_process_course(
    file_path: str,
    module: str,
    course: str,
) -> dict:
    """
    Complete administrator workflow.

    Local PDF
        -> Blob Storage
        -> ingestion
        -> Azure AI Search
    """
    pass