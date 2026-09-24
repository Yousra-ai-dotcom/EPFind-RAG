"""
Course document management routes for EPFind.

These endpoints are intended for course administration.
"""

from fastapi import APIRouter, UploadFile, File, Form


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
    pass


@router.get("")
def get_documents():
    """
    Return all available course documents.
    """
    pass


@router.delete("/{blob_name:path}")
def remove_document(blob_name: str):
    """
    Delete a course document.
    """
    pass