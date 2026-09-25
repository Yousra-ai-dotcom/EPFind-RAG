"""
Routes d'authentification Microsoft Entra ID.
"""

from fastapi import APIRouter, Header, HTTPException

from backend.auth.entra import verify_token

router = APIRouter()


@router.get("/me")
def get_me(authorization: str | None = Header(default=None)):
    """
    Retourne l'identité Microsoft de l'utilisateur connecté.
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token d'authentification manquant.",
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=401,
            detail="Header Authorization invalide.",
        )

    try:
        user = verify_token(token)

        return {
            "authenticated": True,
            "user": user,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error),
        )