import os
from typing import List, Annotated, Dict

from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.security import HTTPBearer

from app.auth import get_user_role, initialize_firebase_admin
from app.dspy_adapter import (
    extract_topics_from_texts,
    generate_topic_tree,
    Topic,
    TopicTree,
    TopicMetadata,
    match_topics_to_material,
    update_topic_tree,
    settings,
)
from app.md_loader import load_markdown_file
import shutil
import sentry_sdk
import logging

logger = logging.getLogger(__name__)

if settings.use_sentry.lower() == "true" and settings.use_sentry_dsn:
    print("Sentry is enabled.")
    sentry_sdk.init(
        dsn=settings.use_sentry_dsn,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Enable sending logs to Sentry
        enable_logs=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profile_session_sample_rate to 1.0 to profile 100%
        # of profile sessions.
        profile_session_sample_rate=1.0,
        # Set profile_lifecycle to "trace" to automatically
        # run the profiler on when there is an active transaction
        profile_lifecycle="trace",
    )


app = FastAPI(title="DSPy Topic Extractor", docs_url="/docs", redoc_url="/redoc", base_url="/topics_extractor")

bearer_scheme = HTTPBearer()



def get_current_user_role(token = Depends(bearer_scheme)) -> str:
    if not token or not token.credentials:
        logger.error('Missing Authorization header')
        raise HTTPException(status_code=403, detail="Missing Authorization header")

    role = get_user_role(token.credentials)
    if not role or role not in ['student', 'teacher']:
        logger.error('Invalid or expired token')
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return role


@app.post("/extract", description="Extract topics from uploaded markdown file")
async def topics(file: UploadFile, user_role: Annotated[str, Depends(get_current_user_role)]):
    if not file:
        raise HTTPException(status_code=400, detail="A file must be provided")
    os.makedirs("temp_files", exist_ok=True)
    file_location = f"temp_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = load_markdown_file(file_location)
    topics = extract_topics_from_texts(text)
    return {"topics": topics, "file_count": 1}


@app.post("/topic_tree", description="Generate a topic tree from uploaded markdown file")
async def topic_tree(file: UploadFile, user_role: Annotated[str, Depends(get_current_user_role)]):
    if not file:
        raise HTTPException(status_code=400, detail="A file must be provided")
    os.makedirs("temp_files", exist_ok=True)
    file_location = f"temp_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = load_markdown_file(file_location)
    topics = extract_topics_from_texts(text)
    topic_tree = generate_topic_tree(topics)
    return {"topic_tree": topic_tree, "file_count": 1}


@app.post("/update_topic_tree", description="Update an existing topic tree with new topics")
async def update_tree(topics: List[Topic], existing_tree: TopicTree, user_role: Annotated[str, Depends(get_current_user_role)]):
    updated_tree = update_topic_tree(existing_tree, topics)
    return {"updated_topic_tree": updated_tree}


@app.get("/test_auth", description="Test authentication and return the user's role")
async def test_auth(user_role: Annotated[str, Depends(get_current_user_role)]):
    return {"role": user_role}

@app.get("/health", description="Check the health status of the service")
async def health():
    return {"status": "ok"}


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

if __name__ == "__main__":
    import uvicorn
    initialize_firebase_admin()
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(settings.port))
    
