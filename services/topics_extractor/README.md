# topics_extractor microservice

A minimal Python microservice (FastAPI) intended to extract topics from free text.

Endpoints

- `GET /health` — returns status
- `POST /extract` — accepts JSON `{ "text": "..." }` and returns `{ "topics": ["...", ...] }`

Run locally (recommended in a venv)

```powershell
cd services/topics_extractor
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Docker

```powershell
# build
docker build -t topics-extractor:local .
# run
docker run -p 8080:8080 topics-extractor:local
```

Notes

- The `extract` endpoint currently contains placeholder logic. Replace with an LLM call, NLP extractor, or a model of your choice.
- If you plan to call external model APIs, store keys in environment variables and inject them via `.env` or your deployment secrets.
