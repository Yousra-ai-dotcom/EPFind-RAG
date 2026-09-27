"""
Routes GET /courses et GET /courses/download

Retourne la liste des cours disponibles dans Azure Blob Storage,
regroupés par module, et permet de télécharger le PDF d'un cours
pour que l'étudiant puisse voir la page exacte citée en source.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from storage.blob_service import list_courses, download_course


router = APIRouter()


@router.get("/courses")
def get_courses():
    """
    Return the list of available EPF courses, and grouped by module.
    """

    try:
        course_documents = list_courses()

        courses = sorted({
            course["course"]
            for course in course_documents
            if course.get("course")
        })

        # Regroupement module -> liste de cours (pour le sélecteur à 2 niveaux)
        modules: dict[str, list[str]] = {}
        for doc in course_documents:
            module = doc.get("module") or "Général"
            course_name = doc.get("course")
            if not course_name:
                continue
            modules.setdefault(module, [])
            if course_name not in modules[module]:
                modules[module].append(course_name)

        for module in modules:
            modules[module].sort()

        return {
            "courses": courses,
            "modules": modules,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la récupération des cours : {str(error)}",
        )


@router.get("/courses/download")
def download_course_pdf(course: str, module: str | None = None):
    """
    Télécharge le PDF d'un cours (utilisé par les sources cliquables du Chat,
    pour permettre à l'étudiant d'ouvrir le vrai document).
    """
    try:
        course_documents = list_courses()

        match = next(
            (
                doc for doc in course_documents
                if doc.get("course") == course

            ),
            None,
        )

        if not match:
            raise HTTPException(
                status_code=404,
                detail=f"Document introuvable pour le cours '{course}'.",
            )

        local_path = download_course(match["blob_name"])

        return FileResponse(
            local_path,
            media_type="application/pdf",
            filename=match.get("document", "cours.pdf"),
            content_disposition_type="inline",  # affiche le PDF dans l'onglet, ne le télécharge pas
        )

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant le téléchargement du document : {str(error)}",
        )
