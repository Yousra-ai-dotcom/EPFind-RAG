"""
Route GET /courses

Retourne la liste des cours disponibles dans Azure Blob Storage
pour alimenter les sélecteurs du frontend EPFind.
"""

from fastapi import APIRouter, HTTPException

from storage.blob_service import list_courses


router = APIRouter()


@router.get("/courses")
def get_courses():
    """
    Return the list of available EPF courses.
    """

    try:
        course_documents = list_courses()

        courses = sorted({
            course["course"]
            for course in course_documents
            if course.get("course")
        })

        return {
            "courses": courses
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la récupération des cours : {str(error)}",
        )