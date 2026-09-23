"""
Authentification Microsoft Entra ID
Responsable : partagé (complété ici pour débloquer la démo)

Le frontend se connecte avec MSAL (Microsoft) et récupère un "access token".
Ce fichier vérifie que ce token est valide et en extrait l'identité
de l'étudiant (nom, email EPF, id Microsoft).

Important : on ne stocke JAMAIS de mot de passe. Microsoft gère tout.
"""

import os
import jwt
from jwt import PyJWKClient
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID")
ENTRA_CLIENT_ID = os.getenv("ENTRA_CLIENT_ID")

# Adresse où Microsoft publie ses clés publiques (pour vérifier la signature
# du token, sans jamais partager de mot de passe).
JWKS_URL = f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/discovery/v2.0/keys"


def verify_token(token: str) -> dict:
    """
    Valide un token JWT émis par Microsoft Entra ID et retourne l'identité
    de l'utilisateur.
    """
    if not ENTRA_TENANT_ID or not ENTRA_CLIENT_ID:
        raise ValueError("ENTRA_TENANT_ID / ENTRA_CLIENT_ID manquants dans .env")

    try:
        jwks_client = PyJWKClient(JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=ENTRA_CLIENT_ID,
            issuer=f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/v2.0",
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Token invalide : {exc}")

    return {
        "name": payload.get("name"),
        "email": payload.get("preferred_username") or payload.get("email"),
        "microsoft_id": payload.get("oid"),
    }


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    """
    Dépendance FastAPI à utiliser dans les routes protégées :
        user: dict = Depends(get_current_user)

    Lit le header "Authorization: Bearer <token>" envoyé par le frontend.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")

    token = authorization.split(" ", 1)[1]
    return verify_token(token)


def get_current_user_optional(authorization: str | None = Header(default=None)) -> dict:
    """
    Variante "souple" utilisée pendant le développement, tant que le login
    Microsoft n'est pas encore branché côté frontend.

    - Si un token est présent -> on le vérifie normalement.
    - Si aucun token n'est présent -> on retourne un utilisateur "invité"
      pour ne pas bloquer la démo (question posée sans être connecté).

    A remplacer par get_current_user (obligatoire) une fois le login
    Microsoft Entra ID branché des deux côtés (frontend + backend).
    """
    if not authorization:
        return {"name": "Invité", "email": "guest@epf.fr", "microsoft_id": "guest"}
    return get_current_user(authorization)
