# Architecture EPF Find

```
                    ÉTUDIANT (compte Microsoft EPF)
                              │
                    Microsoft Entra ID
                              │
                              ▼
                  FRONTEND — Next.js / React / Tailwind
                              │ HTTPS
                              ▼
                    BACKEND — FastAPI
        /auth  /courses  /ask  /summarize  /quiz  /history
                │             │              │
                ▼             ▼              ▼
        Azure AI Search  Azure OpenAI    PostgreSQL
        (RAG / search)   (génération)   (users, historique, QCM)
                │
                ▼
        Azure Blob Storage (PDF des cours)
```

## Pipeline RAG

```
PDF (Azure Blob)
   → PyMuPDF (extraction texte)
   → nettoyage (cleaner.py)
   → chunking (chunker.py)
   → metadata (metadata.py)
   → embeddings (Azure OpenAI)
   → Azure AI Search (index vectoriel + hybride)
   → retrieval (top-k chunks pertinents)
   → prompt (question + contexte)
   → Azure OpenAI (génération)
   → réponse + sources
```

## Ce qu'on n'utilise PAS

ChromaDB, OpenRouter (remplacé par Azure OpenAI dans cette version),
Supabase, Firebase, MongoDB, Microsoft Graph, Streamlit.
