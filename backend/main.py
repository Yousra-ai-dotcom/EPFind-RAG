"""
Backend — point d'entrée FastAPI

Assemble les routes /ask, /courses, /quiz, /summarize, /history
et déclare le endpoint /health.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import ask, courses, quiz, revision, history
from backend.database.database import engine
from backend.database.models import Base

# Crée les tables PostgreSQL si elles n'existent pas encore.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EPF Find API")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
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
