from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi import Form

import shutil
import os

from auth import (
    register_user,
    login_user
)

from orchestrator import (
    chat,
    get_history
)

from rag_manager import (
    upload_document
)

from config import UPLOAD_FOLDER

app = FastAPI(
    title="Conversational AI"
)


@app.get("/")
def home():
    return {
        "message": "Conversational AI API Running"
    }


@app.post("/register")
def register(

    username: str = Form(...),

    email: str = Form(...),

    password: str = Form(...)
):

    return register_user(
        username,
        email,
        password
    )


@app.post("/login")
def login(

    email: str = Form(...),

    password: str = Form(...)
):

    return login_user(
        email,
        password
    )
from fastapi.responses import StreamingResponse

# ----------------------------------------
# Chat Endpoint
# ----------------------------------------

@app.post("/chat")
def chat_api(
    user_id: str = Form(...),
    query: str = Form(...)
):

    return StreamingResponse(
        chat(user_id, query),
        media_type="text/plain"
    )


# ----------------------------------------
# Upload Knowledge File
# ----------------------------------------

@app.post("/upload")
def upload_file(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_document(
        user_id=user_id,
        file_path=file_path
    )

    return {
        "success": True,
        "message": "Document uploaded successfully."
    }


# ----------------------------------------
# Chat History
# ----------------------------------------

@app.get("/history/{user_id}")
def history(user_id: str):

    return get_history(user_id)


# ----------------------------------------
# Health Check
# ----------------------------------------

@app.get("/health")
def health():

    return {
        "status": "Running"
    }


# ----------------------------------------
# Run API
# ----------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )