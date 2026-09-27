"""
Connexion à PostgreSQL pour EPFind.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None

Base = declarative_base()


def get_engine():
    """
    Initialise le moteur PostgreSQL uniquement lorsqu'il est nécessaire.
    """
    global engine

    if engine is None:
        if not DATABASE_URL:
            raise ValueError(
                "DATABASE_URL est manquant dans le fichier .env."
            )

        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
        )

    return engine


def get_session_local():
    """
    Initialise la fabrique de sessions SQLAlchemy à la demande.
    """
    global SessionLocal

    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )

    return SessionLocal


def get_db():
    """
    Fournit une session SQLAlchemy aux routes FastAPI.
    """
    db = get_session_local()()

    try:
        yield db
    finally:
        db.close()