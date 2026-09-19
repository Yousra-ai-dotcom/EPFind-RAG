"""
Backend — point d'entrée FastAPI
Responsable principal : Personne 2

Assemble les routes /ask, /courses, /quiz, /summarize, /history
et déclare le endpoint /health.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import ask, courses, quiz, revision, history

app = FastAPI(title="EPF Find API")

# TODO : restreindre allow_origins à l'URL du frontend en production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask.router)
app.include_router(courses.router)
app.include_router(quiz.router)
app.include_router(revision.router)
app.include_router(history.router)


@app.get("/health")
def health():
    return {"status": "ok"}
