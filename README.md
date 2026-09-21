
# PDF AI Assistant

An intelligent document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

Upload a PDF, ask questions about its content, and receive context-grounded answers with document and page-level source references.

---

## 🚀 Features

- PDF document upload
- Multi-document support
- PDF text extraction using PyMuPDF
- Sentence-aware text chunking
- Semantic embeddings using Sentence Transformers
- ChromaDB vector storage
- Similarity-based semantic retrieval
- LLM-powered question answering
- Source attribution with filename and page number
- Duplicate document protection
- FastAPI REST API
- Upload validation
- 10 MB file-size protection
- Error handling
- Web-based user interface
- OpenRouter LLM integration
- Render deployment support

---

## 🏗️ Architecture

                    ┌─────────────────────┐
                    │      PDF Upload     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PyMuPDF Loader    │
                    │   Text Extraction   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Sentence-Aware     │
                    │     Chunking        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Sentence Transformers│
                    │     Embeddings      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │   Vector Storage    │
                    └──────────┬──────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Query Embedding    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    │       Top-K         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Relevant Chunks   │
                    │ + Page Information  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   OpenRouter LLM    │
                    │ Context-grounded QA │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Answer + Sources   │
                    │ File + Page Number  │
                    └─────────────────────┘

---

## 🧠 How RAG Works

The application follows a complete Retrieval-Augmented Generation pipeline:

1. User uploads a PDF.
2. PyMuPDF extracts the document text.
3. The extracted text is divided into meaningful chunks.
4. Sentence Transformers converts each chunk into a numerical embedding.
5. Embeddings are stored in ChromaDB.
6. The user asks a question.
7. The question is converted into an embedding.
8. ChromaDB searches for the most semantically relevant chunks.
9. Retrieved chunks are provided as context to the LLM.
10. The LLM generates an answer using the retrieved context.
11. The application returns the answer together with document and page-level sources.

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI / Machine Learning

- Sentence Transformers
- all-MiniLM-L6-v2
- Retrieval-Augmented Generation (RAG)
- OpenRouter LLM API

### Document Processing

- PyMuPDF
- Sentence-aware chunking
- Metadata extraction

### Vector Database

- ChromaDB
- Persistent vector storage
- Semantic similarity search

### Frontend

- HTML5
- CSS3
- JavaScript

### Development & Deployment

- Git
- GitHub
- Render
- Environment variables
- REST API

---

## 📂 Project Structure

    PDF-AI-Assistant/
    │
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   │
    │   ├── ingestion/
    │   │   ├── loader.py
    │   │   ├── chunker.py
    │   │   └── embedder.py
    │   │
    │   ├── retrieval/
    │   │   └── retriever.py
    │   │
    │   ├── llm/
    │   │   └── generator.py
    │   │
    │   └── rag/
    │       └── pipeline.py
    │
    ├── frontend/
    │   ├── index.html
    │   ├── style.css
    │   └── script.js
    │
    ├── data/
    │   └── documents/
    │
    ├── vectorstore/
    │
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    ├── render.yaml
    ├── .python-version
    └── README.md

---

## ⚙️ Local Setup

### Clone Repository

    git clone https://github.com/hemanthsurnidi/PDF-AI-Assistant.git
    cd PDF-AI-Assistant

### Create Virtual Environment

    python -m venv venv

### Activate on Windows PowerShell

    venv\Scripts\Activate.ps1

### Install Dependencies

    pip install -r requirements.txt

### Configure Environment Variable

Create a `.env` file containing:

    OPENROUTER_API_KEY=your_api_key_here

Never commit the `.env` file to GitHub.

### Run Application

    uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000/

---

## 🔌 API Endpoints

### Health Check

    GET /health

### Upload PDF

    POST /upload

### Ask Question

    POST /ask

Example question:

    What is the purpose of an information security management system?

---

## 📊 Retrieval Pipeline

    User Question
          │
          ▼
    Query Embedding
          │
          ▼
    ChromaDB Similarity Search
          │
          ▼
    Top-K Relevant Chunks
          │
          ▼
    Context Construction
          │
          ▼
    OpenRouter LLM
          │
          ▼
    Grounded Answer
          │
          ▼
    Source Attribution

---

## 📑 Source Attribution

Each retrieved chunk contains metadata including:

- Filename
- Document ID
- Page number

The final response exposes the relevant document and page information so users can identify where the answer came from.

---

## 📚 Multi-Document Support

The system can index multiple PDF documents inside the same vector database.

Example documents:

- sample.pdf
- security_standard.pdf
- company_policy.pdf
- project_document.pdf

Questions can retrieve relevant information from different indexed documents.

---

## 🛡️ Duplicate Protection

The application prevents the same filename from being indexed repeatedly.

    First Upload
          │
          ▼
      sample.pdf
          │
          ▼
    85 chunks indexed
          │
          ▼
    Second Upload
          │
          ▼
      sample.pdf
          │
          ▼
    Already indexed
          │
          ▼
    0 additional chunks

---

## 🔐 Security & Validation

The application implements:

- PDF extension validation
- Filename sanitization
- 10 MB upload-size limit
- Empty-question validation
- Environment-based API key management
- `.env` excluded from Git
- Failed upload cleanup
- Duplicate-document protection
- Generic API error responses
- CORS configuration

---

## ⚠️ Current Limitations

- Local ChromaDB storage
- Free-tier LLM availability and rate limits
- Some PDFs may contain text-encoding artifacts
- No authentication system
- No user accounts
- Render free-tier filesystem is not persistent
- Uploaded documents may need to be re-indexed after service restarts
- Retrieval quality depends on chunking and embedding quality
- Document identity currently relies on filename
- No reranking layer
- No hybrid BM25 + dense retrieval
- No automated RAG evaluation system
- No production monitoring dashboard

---

## 🚀 Future Improvements

### Retrieval

- Hybrid BM25 + dense retrieval
- Cross-encoder reranking
- Query expansion
- Multi-query retrieval
- Retrieval relevance thresholds

### AI

- Better embedding models
- LLM model selection
- Streaming responses
- Conversation memory
- Agentic document workflows

### Documents

- OCR for scanned PDFs
- Tables and image extraction
- Better encoding handling
- More document formats
- Incremental document updates

### Infrastructure

- Qdrant / Pinecone / hosted vector database
- Persistent cloud storage
- Authentication
- User accounts
- Rate limiting
- Production logging
- Monitoring
- Automated RAG evaluation

---

## ☁️ Deployment

The project is configured for Render deployment.

Build Command:

    pip install -r requirements.txt

Start Command:

    uvicorn app.main:app --host 0.0.0.0 --port $PORT

Required environment variable:

    OPENROUTER_API_KEY

The application can be deployed as a Render web service.

> Note: Render's free filesystem is ephemeral. Local uploaded files and ChromaDB data should not be treated as permanent production storage.

---

## 🧪 Example Use Cases

### Information Security

Upload an information-security standard and ask:

    What is the purpose of the ISMS?

### Company Documents

Upload company policies and ask:

    What is the leave policy?

### Research Papers

Upload a research paper and ask:

    What methodology was used?

### Technical Documentation

Upload technical documentation and ask:

    How does this system work?

---

## 🎯 Project Highlights

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Vector databases
- Semantic search
- Embeddings
- LLM integration
- Document processing
- REST API development
- FastAPI
- Frontend integration
- Source attribution
- Multi-document retrieval
- API security practices
- Git/GitHub workflow
- Cloud deployment preparation

---

## 👨‍💻 Author

**Hemanth Surnidi**

GitHub: https://github.com/hemanthsurnidi

Portfolio: https://hemanthsurnidi.github.io/portfolio/

LinkedIn: https://www.linkedin.com/in/hemanth-surnidi-4a68332b1

---

## 📌 Project Status

**Completed AI Engineering Project**

The project demonstrates an end-to-end RAG system capable of:

    PDF
     ↓
    Extraction
     ↓
    Chunking
     ↓
    Embeddings
     ↓
    Vector Database
     ↓
    Semantic Retrieval
     ↓
    LLM
     ↓
    Grounded Answer
     ↓
    Sources

Built with Python, FastAPI, ChromaDB, Sentence Transformers, PyMuPDF and OpenRouter.

---

## ⭐ Repository

https://github.com/hemanthsurnidi/PDF-AI-Assistant
'@

Set-Content -Path README.md -Value $readme -Encoding UTF8
git add README.md
git commit -m "Improve README documentation"
git push