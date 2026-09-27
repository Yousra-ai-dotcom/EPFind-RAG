# EPFind

EPFind est un assistant pédagogique intelligent destiné aux étudiants de l’EPF.

L’application permet d’interroger et d’exploiter les supports de cours grâce à une architecture **RAG (Retrieval-Augmented Generation)**. Les documents sont stockés, traités, découpés en chunks, enrichis de métadonnées puis indexés afin de permettre aux étudiants de retrouver rapidement une information, poser des questions sur leurs cours, générer des fiches de révision et créer des QCM.

EPFind combine une interface web moderne, une API FastAPI, Microsoft Entra ID, PostgreSQL et plusieurs services Azure.

---

## Fonctionnalités principales

- Authentification avec Microsoft Entra ID
- Identification de l’utilisateur connecté
- Accès aux cours disponibles dans EPFind
- Organisation des contenus par module et par cours
- Chat intelligent basé sur les supports de cours
- Recherche vectorielle dans les documents indexés
- Filtrage des recherches par module et par cours
- Réponses générées à partir du contexte récupéré
- Affichage des sources utilisées dans les réponses
- Sources associées au document et à la page d’origine
- Conversations multiples
- Sauvegarde des conversations et messages
- Historique propre à chaque utilisateur
- Reprise d’une conversation existante
- Génération de fiches de révision
- Génération de QCM
- Correction, score et explication des réponses
- Questions vocales et lecture audio des réponses
- Retour Like / Dislike sur les réponses
- Interface français / anglais
- Thème clair / sombre
- Gestion et indexation des documents PDF
- Tests automatisés du backend, de l’ingestion, du search, de la génération et du stockage

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
| LLM | Azure OpenAI |
| Synthèse / reconnaissance vocale | Azure Speech |
| Base de données | PostgreSQL + SQLAlchemy |
| Stockage des documents | Azure Blob Storage |
| Gestion des secrets | Variables d’environnement / Azure Key Vault |
| Tests | Pytest |
| Versioning | Git + GitHub |

---

## Architecture générale

```text
                         ┌─────────────────────┐
                         │      Étudiant       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Frontend       │
                         │ Next.js / React     │
                         └──────────┬──────────┘
                                    │
                         Microsoft Entra ID
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       PostgreSQL             Pipeline RAG         Azure Blob Storage
   utilisateurs / historique       │                  cours PDF
                                    │
                                    ▼
                            Azure AI Search
                                    │
                                    ▼
                              Azure OpenAI
                                    │
                                    ▼
                           Réponse + sources
```

---

## Architecture RAG

Le pipeline documentaire d’EPFind fonctionne de la manière suivante :

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
(module, cours, document, page)
     ↓
Embeddings
     ↓
Azure AI Search
     ↓
Recherche vectorielle
     ↓
Chunks pertinents
     ↓
Construction du contexte
     ↓
Azure OpenAI
     ↓
Réponse + sources
```

Les documents ne sont pas relus intégralement à chaque question.

Une fois un cours traité, ses chunks et leurs embeddings sont enregistrés dans Azure AI Search. Lorsqu’un étudiant pose une question, EPFind recherche uniquement les passages les plus pertinents avant de construire le contexte transmis au LLM.

Les métadonnées permettent notamment de conserver :

- le module ;
- le cours ;
- le document source ;
- la page d’origine.

Elles permettent également de filtrer la recherche par module ou par cours.

---

## Gestion des documents

Les documents suivent un pipeline complet :

```text
Upload PDF
    ↓
Azure Blob Storage
    ↓
Téléchargement pour traitement
    ↓
Ingestion
    ↓
Extraction + nettoyage
    ↓
Chunking + métadonnées
    ↓
Embeddings
    ↓
Azure AI Search
```

Le dossier `storage/` assure notamment :

- l’upload des cours ;
- le téléchargement des PDF ;
- la liste des documents ;
- la vérification de l’existence d’un cours ;
- la suppression d’un document ;
- le déclenchement du pipeline d’indexation.

Le pipeline évite également de réindexer inutilement un cours déjà présent dans Azure AI Search.

---

## Authentification et utilisateurs

EPFind utilise **Microsoft Entra ID** pour authentifier les utilisateurs.

Le frontend récupère un access token Microsoft puis l’envoie au backend :

```text
Authorization: Bearer <access_token>
```

Le backend vérifie notamment :

- la signature Microsoft du token ;
- le tenant ;
- l’audience ;
- l’expiration ;
- le scope requis.

L’identité Microsoft permet ensuite d’associer les données de l’application à l’utilisateur connecté.

Les utilisateurs sont enregistrés dans PostgreSQL avec notamment :

```text
id
name
email
microsoft_id
created_at
```

---

## Conversations et historique

Chaque conversation appartient à un utilisateur authentifié.

```text
Utilisateur
    ↓
Conversation
    ↓
Messages
 ├── user
 └── assistant
```

Lors du premier message, EPFind crée une conversation et retourne son `conversation_id`.

Les messages suivants peuvent réutiliser cet identifiant afin de continuer la même conversation.

L’historique est filtré selon l’utilisateur connecté : un utilisateur ne peut pas consulter la conversation d’un autre utilisateur.

---

## API Backend

Le frontend communique avec l’application via l’API FastAPI.

| Méthode | Endpoint | Fonction |
|---|---|---|
| GET | `/health` | Vérifier l’état de l’API |
| GET | `/me` | Récupérer l’utilisateur connecté |
| GET | `/courses` | Récupérer les modules et cours disponibles |
| POST | `/ask` | Poser une question au RAG |
| POST | `/summarize` | Générer une fiche de révision |
| POST | `/quiz` | Générer un QCM |
| POST | `/quiz/{quiz_id}/submit` | Corriger un QCM |
| GET | `/history` | Récupérer l’historique de l’utilisateur |
| GET | `/history/{conversation_id}` | Ouvrir une conversation |
| POST | `/feedback` | Enregistrer un Like / Dislike |
| POST | `/speech/transcribe` | Transformer une question audio en texte |
| POST | `/speech/synthesize` | Transformer une réponse en audio |
| GET | `/documents` | Lister les documents |
| POST | `/documents/upload` | Ajouter et traiter un document |
| DELETE | `/documents/{blob_name}` | Supprimer un document |

Le frontend ne communique pas directement avec Azure AI Search ou Azure OpenAI. Ces services sont accessibles via le backend.

---

## Flux d’une question

```text
Étudiant
   ↓
Question
   ↓
Frontend
   ↓
POST /ask
   ↓
Authentification Microsoft
   ↓
FastAPI
   ↓
Utilisateur PostgreSQL
   ↓
Recherche Azure AI Search
   ↓
Chunks pertinents
   ↓
Génération avec Azure OpenAI
   ↓
Réponse + sources
   ↓
Sauvegarde conversation/messages
   ↓
Frontend
```

Exemple simplifié de réponse :

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
  ],
  "conversation_id": 12
}
```

---

# Répartition de l’équipe

## Adam — Ingestion et traitement documentaire

Dossiers principaux :

```text
ingestion/
storage/
```

Responsabilités :

- extraction du texte des PDF avec PyMuPDF ;
- nettoyage du texte ;
- découpage des documents en chunks ;
- préparation des métadonnées ;
- pipeline d’ingestion des documents ;
- préparation des chunks pour l’indexation ;
- participation à la gestion du stockage des cours ;
- intégration du pipeline documentaire avec Azure Blob Storage.

Les métadonnées `module`, `course`, `document` et `page` sont propagées dans le pipeline d’ingestion afin d’être disponibles lors de l’indexation et du retrieval.

---

## Yousra — Search, RAG, Backend et intégration

Dossiers principaux :

```text
search/
backend/
storage/
tests/
```

Responsabilités :

- génération des embeddings ;
- configuration d’Azure AI Search ;
- création et configuration de l’index vectoriel ;
- indexation des chunks ;
- recherche vectorielle ;
- retrieval des passages pertinents ;
- filtrage par module et par cours ;
- intégration du pipeline RAG ;
- développement de l’API FastAPI ;
- connexion entre Search et Generation ;
- gestion des cours et documents côté backend ;
- intégration avec Azure Blob Storage ;
- intégration de PostgreSQL avec SQLAlchemy ;
- gestion des utilisateurs ;
- association des conversations aux utilisateurs authentifiés ;
- gestion de l’historique des conversations ;
- sécurisation de l’accès aux conversations ;
- intégration de Microsoft Entra ID côté backend ;
- validation des access tokens Microsoft ;
- intégration des différents composants du projet ;
- développement et maintenance des tests backend/search/storage.

Yousra est également responsable du repository GitHub, des branches, des merges et de l’intégration globale du projet.

---

## Aya — Génération IA et Frontend avancé

Dossiers principaux :

```text
generation/
frontend/
```

Principalement : Chat, Révision, QCM et composants IA.

Responsabilités :

- intégration du LLM Azure OpenAI ;
- utilisation du modèle `gpt-5-mini` ;
- conception des prompts RAG ;
- génération des réponses à partir du contexte récupéré ;
- génération des résumés et fiches de révision ;
- génération des QCM au format JSON structuré ;
- explication des réponses aux QCM ;
- intégration vocale avec Azure Speech ;
- questions posées à l’oral ;
- lecture des réponses à voix haute ;
- détection français / anglais ;
- système de Like / Dislike sur les réponses ;
- régénération des réponses ;
- affichage des sources et accès au document source ;
- interface Chat ;
- gestion de plusieurs conversations ;
- reprise d’une conversation existante ;
- salutation personnalisée avec le prénom de l’étudiant ;
- sélecteur Module → Cours ;
- interface Révision ;
- interface Quiz ;
- correction et affichage du score ;
- historique unifié Chat / Révision / QCM ;
- identité visuelle de l’application ;
- intégration du frontend avec l’API FastAPI.

---

## Diarra — Structure générale du Frontend

Dossier principal :

```text
frontend/
```

Principalement : structure, navigation et pages secondaires.

Responsabilités :

- développement du dashboard ;
- navigation et Sidebar ;
- interface « Mes cours » ;
- interface Profil ;
- affichage des informations de l’étudiant ;
- thème clair / sombre ;
- choix de la langue ;
- déconnexion ;
- interface CGU ;
- composants généraux de l’application ;
- gestion des états de chargement ;
- gestion des messages d’erreur ;
- système de préférences partagé ;
- système de traduction français / anglais ;
- responsive design ;
- intégration des données fournies par l’API FastAPI.

Aya et Diarra travaillent ensemble sur le frontend avec une répartition des pages et composants afin de limiter les conflits Git.

---

## Structure du projet

```text
epf-find/
│
├── backend/
│   ├── auth/
│   │   └── entra.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── routes/
│   │   ├── ask.py
│   │   ├── auth.py
│   │   ├── courses.py
│   │   ├── documents.py
│   │   ├── feedback.py
│   │   ├── history.py
│   │   ├── quiz.py
│   │   ├── revision.py
│   │   └── speech.py
│   │
│   ├── services/
│   │   ├── history_service.py
│   │   ├── rag_service.py
│   │   ├── revision_service.py
│   │   ├── speech_service.py
│   │   └── user_service.py
│   │
│   └── main.py
│
├── frontend/
│   ├── app/
│   │   ├── chat/
│   │   ├── courses/
│   │   ├── history/
│   │   ├── login/
│   │   ├── profile/
│   │   ├── quiz/
│   │   └── revision/
│   │
│   ├── components/
│   └── lib/
│
├── generation/
│   ├── answer.py
│   ├── llm.py
│   ├── prompts.py
│   └── quiz_generation.py
│
├── ingestion/
│   ├── pdf_loader.py
│   ├── cleaner.py
│   ├── chunker.py
│   ├── metadata.py
│   └── pipeline.py
│
├── search/
│   ├── embeddings.py
│   ├── index.py
│   ├── index_documents.py
│   └── retrieval.py
│
├── storage/
│   ├── blob_service.py
│   └── course_manager.py
│
├── tests/
│   ├── test_backend.py
│   ├── test_generation.py
│   ├── test_ingestion.py
│   ├── test_search.py
│   └── test_storage.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Tests

Les différentes briques du projet disposent de tests automatisés :

```text
Backend
Generation
Ingestion
Search
Storage
```

Pour lancer l’ensemble des tests :

```bash
PYTHONPATH=. pytest tests/ -v
```

Les services Azure sont mockés dans les tests concernés afin d’éviter de modifier les ressources Azure réelles pendant les tests automatisés.

---

## Objectif du prototype

L’objectif d’EPFind est de démontrer un parcours pédagogique complet basé sur le RAG :

```text
Connexion Microsoft
        ↓
Choix du module / cours
        ↓
Question de l’étudiant
        ↓
Recherche des passages pertinents
        ↓
Génération contextualisée
        ↓
Réponse + sources
        ↓
Sauvegarde dans l’historique
```

Autour de ce parcours principal, EPFind propose également la génération de fiches de révision, les QCM, l’interaction vocale et la gestion personnalisée de l’historique.

---

## Équipe

**EPFind — Hackathon IA Générative & Chatbots, EPF Engineering School**

- **Adam Azouzi** — Ingestion et traitement documentaire
- **Yousra Ameur** — Search, RAG, Backend et intégration
- **Aya Ait El Cadi** — Génération IA et Frontend avancé
- **NDIAYE Mame Diarra** — Structure générale du Frontend
