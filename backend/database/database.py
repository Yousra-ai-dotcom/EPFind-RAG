"""
Connexion à PostgreSQL
Responsable : Personne 2 (complété ici pour débloquer la démo)

Ce fichier crée la connexion SQLAlchemy vers la base PostgreSQL et
expose une fonction get_db() utilisable comme dépendance FastAPI.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL est manquant. Ajoutez-le dans votre fichier .env "
        "(ex: postgresql://user:password@host:5432/epffind)"
    )

# L'engine gère le pool de connexions vers PostgreSQL.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal crée une nouvelle "session" (conversation avec la BDD)
# à chaque requête HTTP.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dépendance FastAPI : ouvre une session, la donne à la route,
    puis la ferme automatiquement (même en cas d'erreur).
    Utilisation dans une route : db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
