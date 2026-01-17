# topics_extractor microservice

A Python microservice (FastAPI) intended to extract topics from free text.
It also able to generate topic tree and present topics in a structured way with an option for a UI view.

- Run locally (recommended in a venv)

* Prequisites:
  - Python 3.10+
  - pip
  - .env.local file based on .env.example with proper values

1. Emulator:

```shell
firebase emulators:start
```

2. Local:

```shell
cd services/topics_extractor
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ./app/main.py
```

2. Docker

```powershell
# build
docker build -t topics-extractor:local .
# run
docker run -p 8000:8000 --env-file .\.env.local topics-extractor:local
```

---

## API Docs 🗒️

- To access the API Docs (OpenAPI) use `/docs`
- Example: `http://localhost:8000/docs`

---

## Monitoring with Sentry 🐞

- Sentry is integrated for error tracking and performance monitoring.
- To enable Sentry, set `USE_SENTRY` to `true` and provide a valid `SENTRY_DSN` in your environment variables.
- A test endpoint `/sentry-debug` is available to trigger a test error and verify Sentry integration.
- Dashboard: Once you have Sentry set up, you can monitor errors and performance metrics through the Sentry dashboard.

---

## Notes

- The `extract` endpoint currently contains placeholder logic. Replace with an LLM call, NLP extractor, or a model of your choice.
- If you plan to call external model APIs, store keys in environment variables and inject them via `.env.local` or your deployment secrets.

---
