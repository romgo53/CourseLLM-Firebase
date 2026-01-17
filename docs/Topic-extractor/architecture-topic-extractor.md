# Architecture Spec: topic-extractor

This document describes the topic extractor microservice.
Scope: extract topic lists from Markdown, build topic trees, and match content to topics.

## High-level flow
1) Client obtains a Firebase ID token (role claim required).
2) Client uploads a Markdown file to the microservice with `Authorization: Bearer <token>`.
3) Service reads Markdown, runs DSPy modules against the configured LLM.
4) Service returns topics or a topic tree.

## Component diagram (logical)
```
┌──────────────────────────────┐
│         Client / App         │
│  Uploads Markdown + token    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Topic Extractor (FastAPI)    │
│ - /extract                   │
│ - /topic_tree                │
│ - /update_topic_tree         │                    │
└──────────────┬───────────────┘
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────────┐
│Firebase Admin│  │ DSPy + LLM       │
│ verify token │  │ topic extraction │
└──────────────┘  └──────────────────┘
```

## Topic extraction flow (sequence)
```
Client -> POST /extract (multipart file, Authorization)
FastAPI -> auth.get_user_role(token)
auth -> Firebase Admin (verify token, read role claim)
FastAPI -> md_loader.load_markdown_file(file)
FastAPI -> dspy_adapter.extract_topics_from_texts(text)
FastAPI -> Client (topics JSON)
```

## Components
- **FastAPI app**: `services/topics_extractor/app/main.py` defines endpoints and file upload handling.
- **Auth (Firebase Admin)**: `services/topics_extractor/app/auth.py` verifies ID tokens and reads `custom_claims.role`.
- **Settings**: `services/topics_extractor/app/settings.py` pulls env configuration for LLM and auth.
- **DSPy adapter**: `services/topics_extractor/app/dspy_adapter.py` wraps DSPy calls for extract, tree, match, update.
- **DSPy signatures**: `services/topics_extractor/app/dspy_modules.py` defines the extraction and matching tasks.
- **Models**: `services/topics_extractor/app/models.py` defines `Topic`, `TopicMetadata`, and `TopicTree`.
- **Markdown loader**: `services/topics_extractor/app/md_loader.py` reads Markdown files to text.
- **Topic tree renderer (offline)**: `services/topics_extractor/app/render_topic_tree.py` generates a D3 HTML tree.

## APIs
### POST /extract
- **Auth**: Bearer token required.
- **Body**: `multipart/form-data` with `file` (Markdown).
- **Response**: `{ "topics": [Topic], "file_count": 1 }`

### POST /topic_tree
- **Auth**: Bearer token required.
- **Body**: `multipart/form-data` with `file` (Markdown).
- **Response**: `{ "topic_tree": TopicTree, "file_count": 1 }`

### POST /update_topic_tree
- **Auth**: Bearer token required.
- **Body**: JSON with `topics: Topic[]` and `existing_tree: TopicTree`.
- **Response**: `{ "updated_topic_tree": TopicTree }`

### GET /test_auth
- **Auth**: Bearer token required.
- **Response**: `{ "role": "student" | "teacher" }`

### GET /health
- **Auth**: none.
- **Response**: `{ "status": "ok" }`

## Data model (Pydantic)
### TopicMetadata
- `source_files`: string[] | null
- `confidence_score`: float | null
- `source_sections`: string[] | null

### Topic
- `name`: string
- `description`: string | null
- `metadata`: TopicMetadata | null

### TopicTree
- `topic`: Topic
- `subtopics`: TopicTree[] | null

## Auth and roles
- Tokens are Firebase ID tokens passed via `Authorization: Bearer <token>`.
- `auth.get_user_role` verifies the token and checks `custom_claims.role`.
- Allowed roles: `student`, `teacher`.
- Test hook: `TEST_AUTH_TOKEN` can bypass token verification for local testing.

## Configuration
Environment variables (see `services/topics_extractor/app/settings.py`):
- `PORT` (default 8000)
- `LOG_LEVEL` (default `info`)
- `LM_MODEL` (default `gemini/gemini-2.5-flash`)
- `LM_API_KEY` (LLM provider key)
- `FIREBASE_SERVICE_ACCOUNT_JSON` (service account JSON for Firebase Admin)
- `TEST_AUTH_TOKEN` (optional test token)

## Runtime entry points
- Local dev: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8080`
- Docker: `services/topics_extractor/Dockerfile`
