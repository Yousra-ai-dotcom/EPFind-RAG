"""
Personne 1 — Ingestion
Rôle : découper le texte nettoyé en chunks exploitables par le RAG.

Chaque chunk doit rester assez petit (quelques centaines de mots),
avec éventuellement un léger chevauchement entre chunks consécutifs
pour ne pas couper une idée en plein milieu.
"""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    TODO (Personne 1) :
    - Découper `text` en chunks de ~chunk_size mots
    - Ajouter un chevauchement de `overlap` mots entre deux chunks
    - Retourner la liste des chunks (str)
    """
    raise NotImplementedError
