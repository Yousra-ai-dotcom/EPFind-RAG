# EPFind

EPFind est un assistant intelligent destiné aux étudiants de l’EPF.

L’application permet de consulter et d’exploiter les cours de l’EPF grâce à une architecture RAG (Retrieval-Augmented Generation).

Fonctionnalités principales :

- Authentification avec le compte Microsoft EPF
- Chat intelligent basé sur les cours
- Recherche d’informations dans les supports de cours
- Révision et génération de résumés
- Génération de QCM
- Sélection du module ou du cours
- Explication des réponses aux QCM
- Historique des conversations

---

## Stack technique

| Fonction | Technologie |
|---|---|
| Frontend | Next.js + React + Tailwind CSS |
| Authentification | Microsoft Entra ID |
| Backend / API | FastAPI + Python |
| Lecture PDF | PyMuPDF |
| Embeddings | Azure OpenAI |
| Recherche vectorielle | Azure AI Search |
| LLM | Azure OpenAI / Microsoft Foundry |
| Base de données | PostgreSQL |
| Stockage des cours | Azure Blob Storage |
| Gestion des secrets | Azure Key Vault |
| Tests | Pytest |

---

## Architecture RAG

Le fonctionnement principal de EPFind est :

PDF des cours
→ extraction du texte
→ nettoyage
→ chunking
→ métadonnées
→ embeddings
→ Azure AI Search
→ retrieval
→ contexte
→ LLM
→ réponse

Les mêmes documents pourront être utilisés pour :

- Chat
- Révision
- Résumés
- QCM

---

## Répartition de l'équipe

### Adam — Ingestion

Dossier principal :

`ingestion/`

Responsabilités :

- récupération des PDF
- extraction du texte avec PyMuPDF
- nettoyage du texte
- chunking
- création des métadonnées
- préparation des documents pour l'indexation
- intégration avec Azure Blob Storage

---

### Yousra — Search, RAG et Backend

Dossiers principaux :

`search/`

`backend/`

Responsabilités :

- génération des embeddings
- configuration d'Azure AI Search
- création de l'index vectoriel
- indexation des chunks
- recherche sémantique
- retrieval des passages pertinents
- filtrage par cours/module
- intégration du pipeline RAG
- API FastAPI
- connexion entre ingestion, search et generation
- intégration de l'authentification Microsoft Entra ID

Yousra est également responsable du repository GitHub et de l'intégration du projet.

---

### Aya — Génération IA et Frontend

Dossiers principaux :

`generation/`

`frontend/`

Responsabilités :

- intégration du LLM
- prompts RAG
- génération des réponses
- génération des résumés
- génération des QCM
- explication des réponses
- interface Next.js
- pages Chat, Révision, QCM et Historique
- intégration du frontend avec l'API FastAPI

---

## Structure du projet

```text
epf-find/
├── backend/
├── data/
│   └── courses/
├── docs/
├── frontend/
├── generation/
├── ingestion/
├── search/
├── tests/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md