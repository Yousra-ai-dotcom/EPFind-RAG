from pathlib import Path

from ingestion.pipeline import process_pdf
from search.index_documents import index_documents


COURSES_DIRECTORY = Path("data/courses")


def index_all_courses():
    """
    Parcourt tous les PDF présents dans data/courses,
    lance le pipeline d'ingestion puis indexe les chunks
    dans Azure AI Search.
    """

    pdf_files = list(COURSES_DIRECTORY.rglob("*.pdf"))

    if not pdf_files:
        print("Aucun PDF trouvé dans data/courses.")
        return

    print(f"{len(pdf_files)} PDF trouvé(s).\n")

    for pdf_path in pdf_files:

        # Le premier dossier sous data/courses correspond au module.
        relative_path = pdf_path.relative_to(COURSES_DIRECTORY)

        if len(relative_path.parts) > 1:
            module = relative_path.parts[0]
        else:
            module = "General"

        print("=" * 60)
        print(f"Module : {module}")
        print(f"PDF    : {pdf_path.name}")

        try:
            # Pipeline d'Adam :
            # PDF -> extraction -> nettoyage -> chunks + metadata
            chunks = process_pdf(str(pdf_path))

            if not chunks:
                print("Aucun texte exploitable trouvé.")
                continue

            # On remplace les métadonnées temporaires d'Adam
            # par celles provenant réellement de l'organisation des fichiers.
            for chunk in chunks:
                chunk["module"] = module
                chunk["course"] = pdf_path.stem
                chunk["document"] = pdf_path.name

            print(f"{len(chunks)} chunk(s) généré(s).")

           
            # chunks -> embeddings -> Azure AI Search
            index_documents(chunks)

        except Exception as error:
            print(f"Erreur pendant le traitement de {pdf_path.name} :")
            print(error)

    print("\nIndexation des cours terminée.")


if __name__ == "__main__":
    index_all_courses()
