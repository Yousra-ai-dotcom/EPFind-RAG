# EPFind

EPFind est un assistant intelligent destiné aux étudiants de l’EPF.

L’application permet de consulter et d’exploiter les cours de l’EPF grâce à une architecture RAG (Retrieval-Augmented Generation).

Les cours sont préchargés dans la plateforme par un administrateur et peuvent ensuite être utilisés par les étudiants pour poser des questions, réviser leurs cours et générer des QCM.

## Fonctionnalités principales

- Authentification avec le compte Microsoft EPF
- Accès aux cours disponibles dans EPFind
- Chat intelligent basé sur les cours
- Recherche d’informations dans les supports de cours
- Sélection du module ou du cours
- Révision et génération de résumés
- Génération de QCM
- Explication des réponses aux QCM
- Affichage des sources utilisées dans les réponses
- Historique des conversations
- Gestion et ajout des cours par un administrateur

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

Le fonctionnement principal d’EPFind est :

```text
PDF du cours
      ↓
Azure Blob Storage
      ↓
Extraction du texte
      ↓
Nettoyage
      ↓
Chunking
      ↓
Métadonnées
      ↓
Embeddings
      ↓
Azure AI Search
      ↓
Retrieval
      ↓
Contexte pertinent
      ↓
LLM
      ↓
Réponse + sources
```

Les mêmes documents peuvent être utilisés pour :

- Chat
- Révision
- Résumés
- QCM

### Gestion des cours

Les cours EPF sont ajoutés à la plateforme par un administrateur.

Lorsqu’un nouveau cours est ajouté :

```text
Administrateur
      ↓
Upload du PDF
      ↓
Azure Blob Storage
      ↓
Pipeline d’ingestion
      ↓
Extraction + nettoyage + chunking
      ↓
Embeddings
      ↓
Azure AI Search
      ↓
Cours disponible dans EPFind
```

Pour le prototype du hackathon, un ensemble limité de cours EPF est utilisé afin de démontrer le fonctionnement complet du système.

---

## Répartition de l'équipe

### Adam — Ingestion

Dossier principal :

`ingestion/`

Responsabilités :

- extraction du texte des PDF avec PyMuPDF
- nettoyage du texte
- chunking
- préparation des métadonnées
- préparation des chunks pour l’indexation
- pipeline de traitement des documents

---

### Yousra — Search, RAG et Backend

Dossiers principaux :

`search/`

`backend/`

Responsabilités :

- génération des embeddings
- configuration d’Azure AI Search
- création de l’index vectoriel
- indexation des chunks
- recherche vectorielle et sémantique
- retrieval des passages pertinents
- filtrage par module et cours
- intégration du pipeline RAG
- développement de l’API FastAPI
- connexion entre ingestion, search et generation
- intégration de l’authentification Microsoft Entra ID

Yousra est également responsable du repository GitHub et de l’intégration globale du projet.

---

### Aya — Génération IA et Frontend

Dossiers principaux :

`generation/`

`frontend/`

Responsabilités :

- intégration du LLM
- conception des prompts RAG
- génération des réponses
- génération des résumés
- génération des QCM
- explication des réponses
- développement de l’interface Next.js
- pages Chat, Révision, QCM et Historique
- affichage des réponses et de leurs sources
- intégration du frontend avec l’API FastAPI

---

### Diarra— Course Management & Azure Blob Storage

Dossier principal :

`storage/`


Responsabilités :

- configuration d’Azure Blob Storage
- stockage des PDF des cours
- upload des nouveaux cours
- validation des documents PDF
- récupération de la liste des documents
- téléchargement des documents depuis Azure Blob Storage
- gestion des documents stockés
- organisation des documents par module et cours
- connexion entre Azure Blob Storage et le pipeline d’ingestion
- déclenchement du traitement et de l’indexation d’un nouveau cours

Pipeline associé :

```text
Upload PDF
    ↓
Azure Blob Storage
    ↓
Ingestion
    ↓
Chunks
    ↓
Azure AI Search
    ↓
Cours disponible dans EPFind
```

---

## Structure du projet

```text
epf-find/
├── backend/
│   ├── auth/
│   ├── database/
│   ├── routes/
│   │   ├── ask.py
│   │   ├── courses.py
│   │   ├── documents.py
│   │   ├── history.py
│   │   ├── quiz.py
│   │   └── revision.py
│   ├── services/
│   ├── main.py
│   └── requirements.txt
│
├── data/
│   └── courses/
│
├── docs/
│
├── frontend/
│
├── generation/
│
├── ingestion/
│
├── search/
│
├── storage/
│   ├── __init__.py
│   ├── blob_service.py
│   ├── course_manager.py
│   └── requirements.txt
│
├── tests/
│   └── test_storage.py
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Pipeline global

```text
                   ADMIN
                     │
                     ▼
              Azure Blob Storage
                     │
                     ▼
                  INGESTION
                     │
              PDF → texte → chunks
                     │
                     ▼
               SEARCH / RAG
                     │
        Embeddings → Azure AI Search
                     │
                 Retrieval
                     │
                     ▼
                GENERATION
                     │
                     ▼
               FastAPI Backend
                     │
                     ▼
                  Frontend
                     │
                     ▼
                  Étudiant
```