"""
Route GET /courses
Retourne la liste des cours disponibles (pour remplir le sélecteur de cours
côté frontend).
"""

import os
from fastapi import APIRouter

router = APIRouter()

# Pour le MVP du hackathon, la liste des cours est fixée manuellement.
# Idéalement (amélioration possible), on interroge Azure AI Search pour
# récupérer les valeurs distinctes du champ "course_name".
COURSES = [
    c.strip()
    for c in os.getenv(
        "EPF_COURSES",
        "Machine Learning,Chatbot,Big Data,Blockchain,Java,DevOps"
    ).split(",")
    if c.strip()
]


@router.get("/courses")
def get_courses():
    return {"courses": COURSES}
