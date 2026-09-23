# EPFind

EPFind est un assistant intelligent destiné aux étudiants de l’EPF.

L’application permet de consulter et d’exploiter les cours de l’EPF grâce à une architecture RAG (Retrieval-Augmented Generation).

Les cours sont préparés et indexés dans la plateforme afin de permettre aux étudiants de poser des questions sur leurs cours, générer des fiches de révision et créer des QCM.

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
| Stockage des cours | Azure |
| Gestion des secrets | Variables d’environnement / Azure Key Vault |
| Tests | Pytest |

---

## Architecture RAG

Le fonctionnement principal d’EPFind est :

```text
PDF du cours
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

Les mêmes contenus indexés peuvent être utilisés pour :

- Chat
- Révision
- Résumés
- QCM

Une fois les cours traités et indexés dans Azure AI Search, EPFind peut effectuer les recherches directement dans les contenus indexés sans relire les PDF à chaque question.

Pour le prototype du hackathon, un ensemble limité de cours EPF est utilisé afin de démontrer le fonctionnement complet du système.

---

## Répartition de l'équipe

### Adam — Ingestion

Dossier principal :

`ingestion/`

Responsabilités :

- préparation des documents utilisés par EPFind
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
- recherche vectorielle
- retrieval des passages pertinents
- filtrage par module et cours
- intégration du pipeline RAG
- développement de l’API FastAPI
- endpoints Chat, cours, révision et quiz
- connexion entre Search et Generation
- retour des réponses et de leurs sources au frontend
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
- génération des réponses à partir du contexte récupéré
- génération des résumés
- génération des QCM
- explication des réponses
- développement des fonctionnalités IA du frontend
- interface Chat
- interface Révision
- interface Quiz
- affichage des réponses et de leurs sources
- intégration du frontend avec l’API FastAPI

---

### Diarra — Frontend

Dossier principal :

`frontend/`

Responsabilités :

- développement du dashboard
- navigation et sidebar
- interface "Mes cours"
- interface Historique
- composants généraux de l’application
- gestion des états de chargement
- gestion des messages d’erreur
- responsive design
- intégration des données fournies par l’API FastAPI

Aya et Diarra travaillent ensemble sur le frontend avec une répartition des pages et composants afin de limiter les conflits Git.

---

## Structure du projet

```text
epf-find/
├── backend/
│   ├── auth/
│   │
│   ├── database/
│   │
│   ├── routes/
│   │   ├── ask.py
│   │   ├── courses.py
│   │   ├── history.py
│   │   ├── quiz.py
│   │   └── revision.py
│   │
│   ├── services/
│   │   ├── search_service.py
│   │   ├── rag_service.py
│   │   ├── llm_service.py
│   │   └── quiz_service.py
│   │
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
│   ├── answer.py
│   ├── llm.py
│   ├── prompts.py
│   └── quiz_generation.py
│
├── ingestion/
│
├── search/
│   ├── embeddings.py
│   ├── index.py
│   ├── index_documents.py
│   ├── index_courses.py
│   └── retrieval.py
│
├── storage/
│
├── tests/
│   ├── test_search.py
│   └── test_storage.py
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

Le dossier `storage/` est réservé à l’évolution de la gestion centralisée des documents et n’est pas bloquant pour le MVP du hackathon.

---

## Pipeline global

```text
Cours PDF
    │
    ▼
INGESTION — Adam
PDF → texte → nettoyage → chunks
    │
    ▼
SEARCH — Yousra
Embeddings → Azure AI Search
    │
    │
    └─────────────────────────────┐
                                  │
Étudiant                          │
    │                             │
    ▼                             │
Frontend — Aya / Diarra           │
    │                             │
    ▼                             │
FastAPI Backend — Yousra          │
    │                             │
    ├── GET /courses              │
    │                             │
    ├── POST /ask ─► Retrieval ◄──┘
    │                    │
    │                    ▼
    │             Chunks pertinents
    │                    │
    │                    ▼
    │             GENERATION — Aya
    │                    │
    │                    ▼
    │               Azure OpenAI
    │                    │
    ◄──────────── Réponse + sources
    │
    ▼
Frontend
    │
    ▼
Étudiant
```

---

## API Backend

Le frontend communique uniquement avec l’API FastAPI.

Endpoints principaux prévus :

| Méthode | Endpoint | Fonction |
|---|---|---|
| GET | `/health` | Vérifier l’état de l’API |
| GET | `/courses` | Récupérer les cours disponibles |
| POST | `/ask` | Poser une question sur un cours |
| POST | `/revision` | Générer une fiche de révision |
| POST | `/quiz` | Générer un QCM |
| GET | `/history` | Consulter l’historique |

Le frontend ne communique pas directement avec Azure AI Search ou Azure OpenAI.

---

## Flux d’une question RAG

```text
Étudiant
   ↓
Question + module/cours
   ↓
POST /ask
   ↓
FastAPI
   ↓
Retrieval Azure AI Search
   ↓
Chunks pertinents
   ↓
Prompt + LLM
   ↓
Réponse
   +
Sources
   ↓
Frontend
```

Exemple de réponse de l’API :

```json
{
  "answer": "Un commit Git représente...",
  "sources": [
    {
      "module": "GIT",
      "course": "Les commits",
      "document": "cours.pdf",
      "page": 5
    }
  ]
}
```

---

## Objectif du prototype

L’objectif principal du prototype est de démontrer un parcours RAG complet :

```text
Choisir un cours
      ↓
Poser une question
      ↓
Rechercher les passages pertinents
      ↓
Générer une réponse à partir des cours
      ↓
Afficher la réponse et ses sources
```

Les fonctionnalités Révision, Quiz, Historique et authentification viennent compléter ce parcours principal.
