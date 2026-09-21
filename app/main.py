from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.rag.pipeline import ask_question
from app.ingestion.embedder import ingest_pdf


app = FastAPI(
    title="Intelligent PDF Question Answering System",
    description="RAG-based PDF question answering API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MAX_FILE_SIZE = 10 * 1024 * 1024


# Serve CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "PDF AI Assistant"
    }


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        answer, sources = ask_question(
            request.question
        )

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to process the question"
        )


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    filename = Path(file.filename).name

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    file_data = await file.read()

    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit"
        )

    file_path = DOCUMENTS_DIR / filename

    try:

        with open(file_path, "wb") as buffer:
            buffer.write(file_data)

        chunk_count = ingest_pdf(
            str(file_path),
            filename
        )

        if chunk_count == 0:

            return {
                "filename": filename,
                "message": "PDF was already indexed",
                "chunks": 0
            }

        return {
            "filename": filename,
            "message": "PDF uploaded and indexed successfully",
            "chunks": chunk_count
        }

    except Exception:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Failed to process PDF"
        )