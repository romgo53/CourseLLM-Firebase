import os
from typing import List, Annotated, Dict

from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel

from auth import verify_token as verify_firebase_token, get_user_role, initialize_firebase_admin
from utils import get_course_topics
from dspy_adapter import extract_topics_from_texts, generate_topic_tree, Topic, TopicTree,TopicMetadata, match_topics_to_material, update_topic_tree
from md_loader import load_markdown_file
from file_store_fecher import fetch_markdown_files
from pprint import pprint
import shutil

app = FastAPI(title="DSPy Topic Extractor", docs_url="/docs", redoc_url="/redoc", base_url="/topics_extractor")

bearer_scheme = HTTPBearer()



def get_current_user_role(token = Depends(bearer_scheme)) -> str:
    if not token or not token.credentials:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    role = get_user_role(token.credentials)
    if not role or role not in ['student', 'teacher']:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return role


@app.post("/extract")
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


@app.post("/topic_tree")
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


@app.post("/update_topic_tree")
async def update_tree(topics: List[Topic], existing_tree: TopicTree, user_role: Annotated[str, Depends(get_current_user_role)]):
    updated_tree = update_topic_tree(existing_tree, topics)
    return {"updated_topic_tree": updated_tree}


@app.post("/match")
async def match_topics(course_id: str, file: UploadFile, user_role: Annotated[str, Depends(get_current_user_role)]):
    if not file:
        raise HTTPException(status_code=400, detail="A file must be provided")
    os.makedirs("temp_files", exist_ok=True)
    file_location = f"temp_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = load_markdown_file(file_location)
   
    topics = [
        Topic(name="Advanced Problem-Solving Techniques",
              description="Comprehensive methods and strategies for tackling complex computational challenges, including self-referential approaches and optimization techniques.",
              metadata=TopicMetadata(
                  source_files=["None"],
                  confidence_score=0.95,
                  source_sections=None
              )),
        Topic(name="Self-Referential Solutions",
                description="A powerful problem-solving approach that involves breaking down a problem into smaller instances of the same problem, typically implemented through recursion.",
                metadata=TopicMetadata(
                    source_files=["None"],
                    confidence_score=0.95,
                    source_sections=None
                )),
        Topic(name="Recursive Problem Components",
                description="The essential elements required for a functional self-referential (recursive) solution, including a termination condition (base case), a reduction step, and combination logic.",
                metadata=TopicMetadata(
                    source_files=["None"],
                    confidence_score=0.95,
                    source_sections=None
                ))
    
    ]
    matched_topics = match_topics_to_material(text, topics)
    return {"matched_topics": matched_topics, "file_count": 1}
   

@app.get("/test_auth")
async def test_auth(user_role: Annotated[str, Depends(get_current_user_role)]):
    return {"role": user_role}

@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    initialize_firebase_admin()
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000)))
    
