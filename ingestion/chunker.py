"""
Personne 1 — Ingestion

Rôle : découper le texte nettoyé en chunks exploitables par le RAG.

Chaque chunk doit rester assez petit (quelques centaines de mots),
avec éventuellement un léger chevauchement entre chunks consécutifs
pour ne pas couper une idée en plein milieu.
"""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Découpe un texte en chunks de `chunk_size` mots avec
    un chevauchement de `overlap` mots entre les chunks.

    Args:
        text: Texte nettoyé à découper.
        chunk_size: Nombre maximum de mots par chunk.
        overlap: Nombre de mots communs entre deux chunks.

    Returns:
        Liste des chunks sous forme de chaînes de caractères.

    Raises:
        ValueError: Si les paramètres sont invalides.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size doit être supérieur à 0.")

    if overlap < 0:
        raise ValueError("overlap ne peut pas être négatif.")

    if overlap >= chunk_size:
        raise ValueError("overlap doit être inférieur à chunk_size.")

    if not text or not text.strip():
        return []

    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]

        if not chunk_words:
            break

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        # Le dernier chunk est atteint.
        if start + chunk_size >= len(words):
            break

    return chunks


if __name__ == "__main__":
    # Exemple de test
    text = " ".join(f"mot{i}" for i in range(1, 1201))

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=50,
    )

    print(f"Nombre de chunks : {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(f"Nombre de mots : {len(chunk.split())}")
        print(f"Début : {chunk[:100]}...")