# Qui code quoi

## Personne 1 — Ingestion des cours
Dossier : `ingestion/`
- `pdf_loader.py` : lire les PDF
- `cleaner.py` : nettoyer le texte (espaces, headers/footers, caractères)
- `chunker.py` : découper le texte en chunks
- `metadata.py` : ajouter course / module / chapter / page
- `upload_blob.py` : uploader les PDF vers Azure Blob Storage

## Personne 2 — Embeddings + Azure AI Search + intégration backend
Dossiers : `search/`, `backend/` (intégration)
- `search/embeddings.py` : transformer les chunks en vecteurs
- `search/index.py` : créer/gérer l'index Azure AI Search
- `search/retrieval.py` : recherche vectorielle/hybride + filtre par cours
- `backend/main.py`, `backend/routes/*`, `backend/database/*` : API FastAPI + PostgreSQL

## Personne 3 — Prompt + LLM + génération + frontend
Dossiers : `generation/`, `frontend/` (responsable principal)
- `generation/prompts.py` : tous les prompts (Q&A, résumé, QCM)
- `generation/llm.py` : connexion Azure OpenAI
- `generation/answer.py` : question + contexte → réponse + sources
- `generation/quiz_generator.py` : génération des QCM en JSON
- `frontend/app/*`, `frontend/components/*` : pages et composants Next.js

## Tout le monde
- `docs/`, `tests/`, login Entra, déploiement Azure, revue de code mutuelle.
