import os
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

from .auth import verify_firebase_token
from dspy_adapter import extract_topics_from_texts, match_topics_from_to_material



app = FastAPI(title="DSPy Topic Extractor", docs_url="/docs", redoc_url="/redoc")


class FilesRequest(BaseModel):
    file_ids: List[str]


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization.split(" ", 1)[1].strip()
    decoded = verify_firebase_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return decoded


@app.post("/topics")
async def topics(request: FilesRequest, user: dict = Depends(get_current_user)):
    if not request.file_ids:
        raise HTTPException(status_code=400, detail="file_ids must be a non-empty list")
    files = fetch_markdown_files(request.file_ids)
    if not files:
        raise HTTPException(status_code=404, detail="No files fetched; check IDs or service account permissions")
    texts = list(files.values())
    topics = extract_topics_from_texts(texts[0])
    return {"topics": topics, "file_count": len(files)}



@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000)))