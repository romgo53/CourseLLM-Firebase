import os
from typing import List, Annotated

from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel

from auth import verify_token as verify_firebase_token, get_user_role, initialize_firebase_admin
from utils import get_course_topics
from dspy_adapter import extract_topics_from_texts, generate_topic_tree, Topic, TopicTree, match_topics_to_material
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
    file_location = f"temp_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = load_markdown_file(file_location)
    topics = extract_topics_from_texts(text)
    return {"topics": topics, "file_count": 1}


@app.post("/match")
async def match_topics(file: UploadFile, course_id: str, user_role: Annotated[str, Depends(get_current_user_role)]):
    if not file:
        raise HTTPException(status_code=400, detail="A file must be provided")
    file_location = f"temp_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = load_markdown_file(file_location)
    topics = await get_course_topics(course_id)
    topic_tree = generate_topic_tree(topics)
    matched_topics = match_topics_to_material(text, topics)
    return {"topics": topics, "topic_tree": topic_tree, "matched_topics": matched_topics, "file_count": 1}
   

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
    


# def run_example():
#     text = load_markdown_file("topic_01_advanced_techniques.md")
#     print("Loaded text length:", len(text))
#     topics_res: List[Topic] | None = extract_topics_from_texts(text)
#     print("Extracted topics:", topics_res)
#     topic_tree: TopicTree | None  = generate_topic_tree(topics_res)
#     print("Generated topic tree:", topic_tree)



# if __name__ == "__main__":
#     import asyncio
#     run_example()

# // eyJhbGciOiJSUzI1NiIsImtpZCI6ImEzOGVhNmEwNDA4YjBjYzVkYTE4OWRmYzg4ODgyZDBmMWI3ZmJmMGUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoicm9tIGdvcmVuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xCa2hPUUduSHFlOVdlb3hDejhVRjIyTjR0YU1iN0RKQnJaQl80bThmQTl0aDFYR01OUUE9czk2LWMiLCJyb2xlIjoic3R1ZGVudCIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb3Vyc2UtbGxtLWZpcmViYXNlIiwiYXVkIjoiY291cnNlLWxsbS1maXJlYmFzZSIsImF1dGhfdGltZSI6MTc2NjkzMDg1MywidXNlcl9pZCI6Im1Xb1owRHVycHBaWGc1eVk1SFV1aTRSblFmVDIiLCJzdWIiOiJtV29aMER1cnBwWlhnNXlZNUhVdWk0Um5RZlQyIiwiaWF0IjoxNzY2OTMwODUzLCJleHAiOjE3NjY5MzQ0NTMsImVtYWlsIjoicm9tZ281M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwMzYzMjc3MDczMzY4ODY2MjcyNyJdLCJlbWFpbCI6WyJyb21nbzUzQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.nJbWDUFx7H-Y9rNN8y2n94gVCU7RE6xviSgrSumQ29vzwJRlvjGCPsLZWVAJdm9p5jt-_Xl7UweKbhPavGBR37qMb-8a0n7Lie5c4IiD_fbnMDOKXsAnleyBKNXGBzmmbB6UcXffBK_HNVUWJ-xf7mS6WYoPW2OKQK7-6eCn27RNdxxWcB0aBKgcssDmsDGqLk5-PYy0k5W3PByjUgR0dl2qBWgNYe40H7FspUnInTFA03uPDY_JyjK2X0gXz9-QJ7VqWqL-ZVsTqvtNfpvc-GdI3DHjBdrLtci9Ccj6I4aXMDsNfElOqrxUQO13BmokSwd3SXXLFtxIii8WVUGh4w