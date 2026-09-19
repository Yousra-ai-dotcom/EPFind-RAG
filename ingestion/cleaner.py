"""
Personne 1 — Ingestion
Rôle : nettoyer le texte brut extrait des PDF.

À supprimer/normaliser :
- espaces multiples et sauts de ligne inutiles
- caractères bizarres issus de l'extraction PDF
- headers/footers répétés sur chaque page
- numéros de page isolés
"""


def clean_text(raw_text: str) -> str:
    """
    TODO (Personne 1) :
    - Normaliser les espaces
    - Retirer les headers/footers récurrents
    - Retourner le texte nettoyé
    """
    raise NotImplementedError
