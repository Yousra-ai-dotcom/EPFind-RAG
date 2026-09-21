"""
Personne 1 — Ingestion
Rôle : nettoyer le texte brut extrait des PDF.

À supprimer/normaliser :
- espaces multiples et sauts de ligne inutiles
- caractères bizarres issus de l'extraction PDF
- headers/footers répétés sur chaque page
- numéros de page isolés
"""

import re
import unicodedata
from collections import Counter


def clean_text(raw_text: str) -> str:
    """
    Nettoie et normalise le texte extrait d'un PDF.

    Args:
        raw_text: Texte brut extrait d'un PDF.

    Returns:
        Texte nettoyé et normalisé.
    """

    if not isinstance(raw_text, str):
        raise TypeError("raw_text doit être une chaîne de caractères.")

    if not raw_text.strip():
        return ""

    # ---------------------------------------------------------
    # 1. Normalisation Unicode
    # ---------------------------------------------------------
    text = unicodedata.normalize("NFKC", raw_text)

    # ---------------------------------------------------------
    # 2. Suppression de certains caractères invisibles
    # ---------------------------------------------------------
    text = text.replace("\u00ad", "")  # soft hyphen
    text = text.replace("\u200b", "")  # zero-width space
    text = text.replace("\ufeff", "")  # BOM

    # ---------------------------------------------------------
    # 3. Normalisation des espaces
    # ---------------------------------------------------------
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remplace les espaces et tabulations multiples par un espace.
    text = re.sub(r"[ \t]+", " ", text)

    # Supprime les espaces en début/fin de chaque ligne.
    lines = [line.strip() for line in text.split("\n")]

    # ---------------------------------------------------------
    # 4. Suppression des lignes vides consécutives
    # ---------------------------------------------------------
    cleaned_lines = []

    for line in lines:
        if line:
            cleaned_lines.append(line)

    # ---------------------------------------------------------
    # 5. Suppression des numéros de page isolés
    # ---------------------------------------------------------
    # Exemples supprimés :
    # 1
    # 12
    # 125
    # - 12 -
    # Page 12
    # Page 12 / 50
    page_number_pattern = re.compile(
        r"^(?:page\s*)?(?:[-–—]\s*)?\d+"
        r"(?:\s*[/\-]\s*\d+)?"
        r"(?:\s*[-–—])?$",
        re.IGNORECASE,
    )

    filtered_lines = []

    for line in cleaned_lines:
        if page_number_pattern.match(line):
            continue

        filtered_lines.append(line)

    # ---------------------------------------------------------
    # 6. Détection des headers/footers répétés
    # ---------------------------------------------------------
    # Une ligne qui apparaît plusieurs fois exactement peut
    # correspondre à un header ou un footer de page.
    line_counts = Counter(filtered_lines)

    repeated_lines = {
        line
        for line, count in line_counts.items()
        if count >= 3 and len(line) < 150
    }

    final_lines = [
        line
        for line in filtered_lines
        if line not in repeated_lines
    ]

    # ---------------------------------------------------------
    # 7. Nettoyage des caractères parasites
    # ---------------------------------------------------------
    cleaned_text = "\n".join(final_lines)

    # Réduit les espaces multiples restants.
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

    # Réduit les sauts de ligne excessifs.
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    # Supprime les espaces avant/après les sauts de ligne.
    cleaned_text = re.sub(r" *\n *", "\n", cleaned_text)

    return cleaned_text.strip()