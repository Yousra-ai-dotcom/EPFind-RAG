"""
Point d'entrée de l'API FastAPI d'EPFind.

Le backend expose les endpoints utilisés par le frontend
et orchestre les différentes briques du système RAG.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import ask, courses, quiz, revision
load_dotenv()

app = FastAPI(
    title="EPFind API",
    description="API backend de l'assistant pédagogique EPFind",
    version="1.0.0",
)

# URL du frontend Next.js.
# En développement, Next.js utilise généralement le port 3000.
frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ask.router)
app.include_router(courses.router)
app.include_router(quiz.router)
app.include_router(revision.router)


@app.get("/")
def root():
    return {
        "name": "EPFind API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }