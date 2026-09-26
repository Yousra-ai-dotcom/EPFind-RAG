"""
Route GET /courses

Retourne la liste des cours disponibles dans Azure Blob Storage
pour alimenter les sélecteurs du frontend EPFind.

NOTE (ajout Aya - Personne 3) : le champ "modules" a été ajouté en plus
de "courses" (qui reste inchangé, pour ne rien casser côté Diarra/main)
afin d'alimenter le sélecteur Module -> Cours du Chat et de la Révision.
A valider avec Yousra, responsable officielle de ce fichier.
"""

from fastapi import APIRouter, HTTPException

from storage.blob_service import list_courses


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
