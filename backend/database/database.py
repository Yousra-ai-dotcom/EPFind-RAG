"""
Connexion à PostgreSQL
Responsable : Personne 2
"""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# TODO (Personne 2) :
# - Créer l'engine SQLAlchemy avec DATABASE_URL
# - Créer SessionLocal (sessionmaker)
# - Exposer une fonction get_db() utilisable comme dépendance FastAPI
