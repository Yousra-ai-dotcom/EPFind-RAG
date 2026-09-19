"""
Authentification Microsoft Entra ID
Responsable : partagé (mise en place initiale : Personne 2 ou 3)

Vérifie le token Microsoft envoyé par le frontend après connexion,
et en extrait l'identité de l'étudiant (nom, email EPF, id Microsoft).
Ne jamais stocker de mot de passe : Microsoft gère l'authentification.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID")
ENTRA_CLIENT_ID = os.getenv("ENTRA_CLIENT_ID")


def verify_token(token: str) -> dict:
    """
    TODO :
    - Valider le token JWT reçu du frontend (signature, tenant, audience)
    - Retourner {"name": ..., "email": ..., "microsoft_id": ...}
    """
    raise NotImplementedError
