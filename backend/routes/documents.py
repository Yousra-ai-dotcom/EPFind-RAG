"""
Course document management routes for EPFind.

These endpoints are intended for course administration.
"""

import os
import tempfile
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from storage.blob_service import delete_course, list_courses
from storage.course_manager import upload_and_process_course
from search.retrieval import delete_indexed_course


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    module: str = Form(...),
    course: str = Form(...),
):
    """
    Upload and process a new EPF course.
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Nom de fichier manquant.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être un PDF.",
        )

    temp_path = None

    try:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        result = upload_and_process_course(
            file_path=temp_path,
            module=module,
            course=course,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant l'import du document : {str(error)}",
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("")
def get_documents():
    """
    Return all available course documents.
    """
    try:
        return list_courses()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la récupération des documents : {str(error)}",
        )


@router.delete("/{blob_name:path}")
def remove_document(blob_name: str):
    """
    Delete a course document from Azure Blob Storage
    and remove its indexed chunks from Azure AI Search.
    """
    try:
        # blob_name attendu : <module>/<course>.pdf
        if "/" not in blob_name:
            raise ValueError(
                "Le nom du blob doit contenir le module et le document."
            )

        module, filename = blob_name.split("/", 1)

        course = (
            filename[:-4]
            if filename.lower().endswith(".pdf")
            else filename
        )

        # Vérifier/supprimer le PDF du Blob Storage.
        deleted = delete_course(blob_name)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Document introuvable.",
            )

        # Supprimer également les chunks Azure AI Search.
        deleted_chunks = delete_indexed_course(
            module=module,
            course=course,
        )

        return {
            "deleted": True,
            "blob_name": blob_name,
            "deleted_chunks": deleted_chunks,
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la suppression du document : {str(error)}",
        )