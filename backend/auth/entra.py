"""
Authentification Microsoft Entra ID pour EPF Find.

Valide l'access token envoyé par le frontend et récupère
l'identité de l'utilisateur connecté.
"""

import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException
from jose import JWTError, jwt
import requests


load_dotenv()

ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID")
ENTRA_CLIENT_ID = os.getenv("ENTRA_CLIENT_ID")



MICROSOFT_LOGIN = "https://" + "login.microsoftonline.com"




def verify_token(token: str) -> dict:
    """
    Vérifie un access token Microsoft Entra ID.

    Vérifications :
    - signature Microsoft
    - audience EPF Find
    - issuer / tenant
    - expiration
    - scope access_as_user

    Retourne l'identité de l'utilisateur.
    """
    if not ENTRA_TENANT_ID:
        raise ValueError("ENTRA_TENANT_ID est manquant.")

    if not ENTRA_CLIENT_ID:
        raise ValueError("ENTRA_CLIENT_ID est manquant.")

    issuer = f"{MICROSOFT_LOGIN}/{ENTRA_TENANT_ID}/v2.0"

    jwks_url = (
        f"{MICROSOFT_LOGIN}/{ENTRA_TENANT_ID}/"
        "discovery/v2.0/keys"
    )

    try:
        # Récupération des clés publiques Microsoft
        jwks = requests.get(jwks_url, timeout=5)
        jwks.raise_for_status()
        keys = jwks.json()

        # Lecture du header JWT pour trouver la clé utilisée
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        rsa_key = next(
            (key for key in keys["keys"] if key.get("kid") == kid),
            None,
        )

        if rsa_key is None:
            raise ValueError("Clé de signature Microsoft introuvable.")

        # Vérification cryptographique du token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=ENTRA_CLIENT_ID,
            issuer=issuer,
        )

        # Vérification du scope
        scopes = payload.get("scp", "").split()

        if "access_as_user" not in scopes:
            raise ValueError(
                "Le token ne possède pas le scope access_as_user."
            )

        # Identité Microsoft
        microsoft_id = payload.get("oid") or payload.get("sub")
        name = payload.get("name", "")
        email = (
            payload.get("preferred_username")
            or payload.get("email")
            or payload.get("upn")
        )

        if not microsoft_id:
            raise ValueError(
                "Identifiant Microsoft absent du token."
            )

        if not email:
            raise ValueError(
                "Adresse utilisateur absente du token."
            )

        return {
            "name": name,
            "email": email,
            "microsoft_id": microsoft_id,
        }

    except (JWTError, ValueError, KeyError) as exc:
        raise ValueError(
            f"Token Microsoft invalide : {exc}"
        ) from exc


def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict:
    """
    Dépendance FastAPI pour les routes protégées.

    Lit le header Authorization: Bearer <token>.
    """

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")

    token = authorization.split(" ", 1)[1]
    return verify_token(token)


def get_current_user_optional(
    authorization: str | None = Header(default=None),
) -> dict:
    """
    Variante souple utilisée pendant le développement.

    Si aucun token n'est présent, retourne un utilisateur invité.
    """

    if not authorization:
        return {
            "name": "Invité",
            "email": "guest@epf.fr",
            "microsoft_id": "guest",
        }

    return get_current_user(authorization)