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

from ingestion.pipeline import process_pdf
from search.index_documents import index_documents
from search.retrieval import course_is_indexed
from storage.blob_service import (
    download_course,
    list_courses,
    upload_course,
)

def prepare_course_chunks(
    pdf_path: str,
    module: str,
    course: str,
) -> list[dict]:
    """
    Process a PDF using the existing ingestion pipeline
    and add the required EPFind metadata to every chunk.
    """

    chunks = process_pdf(pdf_path)

    for chunk in chunks:
        chunk["module"] = module
        chunk["course"] = course

    return chunks


def index_course(
    pdf_path: str,
    module: str,
    course: str,
) -> dict:
    """
    Process a local course PDF and index its chunks
    into Azure AI Search.
    """

    chunks = prepare_course_chunks(
        pdf_path=pdf_path,
        module=module,
        course=course,
    )

    if not chunks:
        return {
            "module": module,
            "course": course,
            "chunks": 0,
            "indexed": False,
        }

    results = index_documents(chunks)

    successful = sum(
        1 for result in results
        if result.succeeded
    )

    return {
        "module": module,
        "course": course,
        "chunks": len(chunks),
        "indexed_chunks": successful,
        "indexed": successful == len(chunks),
    }


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

    pdf_path = download_course(blob_name)

    result = index_course(
        pdf_path=pdf_path,
        module=module,
        course=course,
    )

    result["blob_name"] = blob_name

    return result


def process_all_courses() -> list[dict]:
    """
    Process and index only courses that are not already
    present in Azure AI Search.
    """

    courses = list_courses()

    if not courses:
        print("Aucun cours trouvé dans Azure Blob Storage.")
        return []

    results = []

    print(f"{len(courses)} cours trouvé(s) dans Azure Blob Storage.\n")

    for course_info in courses:

        blob_name = course_info["blob_name"]
        module = course_info["module"]
        course = course_info["course"]

        print("=" * 60)
        print(f"Module : {module}")
        print(f"Cours  : {course}")

        try:
            # Ne pas recalculer les embeddings d'un cours déjà indexé
            if course_is_indexed(module, course):
                print("Déjà indexé -> ignoré.")

                results.append({
                    "blob_name": blob_name,
                    "module": module,
                    "course": course,
                    "status": "skipped",
                })

                continue

            print("Nouveau cours -> indexation...")

            result = process_course(
                blob_name=blob_name,
                module=module,
                course=course,
            )

            result["status"] = "indexed"
            results.append(result)

        except Exception as error:
            print(f"Erreur : {error}")

            results.append({
                "blob_name": blob_name,
                "module": module,
                "course": course,
                "status": "error",
                "error": str(error),
            })

    return results
    


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

    upload_result = upload_course(
        file_path=file_path,
        module=module,
        course=course,
    )

    blob_name = upload_result["blob_name"]

    processing_result = process_course(
        blob_name=blob_name,
        module=upload_result["module"],
        course=upload_result["course"],
    )

    return {
        **upload_result,
        **processing_result,
    }