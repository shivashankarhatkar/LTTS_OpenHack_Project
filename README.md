# Enterprise Knowledge Assistant

An enterprise-grade AI-powered knowledge management platform that combines **GraphRAG**, **Hybrid Retrieval**, **Knowledge Graphs**, and **LangGraph** to deliver accurate, explainable, and citation-backed answers from organizational knowledge.

The system transforms unstructured enterprise documents into structured knowledge by extracting entities, relationships, policies, and claims while maintaining a vector database for semantic retrieval. By combining symbolic reasoning from a Knowledge Graph with semantic search from Vector Retrieval, the assistant provides reliable responses with confidence scoring and hallucination validation.

---

# Features

## Enterprise Document Ingestion

- PDF support
- DOCX support
- PPTX support
- Automatic text extraction
- Intelligent document chunking
- Metadata extraction
- Embedding generation
- ChromaDB indexing
- Neo4j Knowledge Graph generation

---

## Knowledge Graph

- Automatic entity extraction
- Relationship extraction
- Entity resolution
- Ontology mapping
- Graph traversal
- Graph search
- Graph-based retrieval

---

## Hybrid Retrieval

The retrieval engine combines multiple retrieval techniques.

- Dense Vector Retrieval
- Knowledge Graph Retrieval
- Keyword (BM25) Retrieval
- Context Fusion
- Result Re-ranking

This significantly improves retrieval accuracy over traditional RAG systems.

---

## GraphRAG

GraphRAG combines semantic retrieval with graph reasoning.

Pipeline


User Query
      │
      ▼
Hybrid Retriever
      │
      ▼
Context Builder
      │
      ▼
Prompt Builder
      │
      ▼
Gemini
      │
      ▼
Answer Generations

---

## LangGraph Multi-Agent Workflow

The assistant uses LangGraph for orchestration.

```text
                 User Query
                      │
                      ▼
               Router Agent
              ┌──────────────┐
              ▼              ▼
     Document QA        Graph QA
              │              │
              └──────┬───────┘
                     ▼
            Summarization Agent
                     ▼
              Citation Agent
                     ▼
             Validation Agent
                     ▼
               Final Response
```

---

## Enterprise Features

- Multi-agent architecture
- GraphRAG
- Hybrid Retrieval
- Knowledge Graph
- Citation generation
- Confidence scoring
- Hallucination detection
- Conversation memory
- Institutional memory
- JWT Authentication
- Audit logging
- REST APIs
- Docker support

---

# Architecture

```text
                        Frontend
                           │
                           ▼
                      FastAPI APIs
                           │
                           ▼
                     Chat Service
                           │
                           ▼
                   LangGraph Workflow
                           │
      ┌────────────────────┴────────────────────┐
      ▼                                         ▼
Document QA Agent                       Graph QA Agent
      │                                         │
      └────────────────────┬────────────────────┘
                           ▼
                    Hybrid Retriever
        ┌────────────┬──────────────┬─────────────┐
        ▼            ▼              ▼
    Vector DB   Knowledge Graph   Keyword Search
        │            │              │
        └────────────┴──────────────┘
                     ▼
              Context Builder
                     ▼
              Prompt Builder
                     ▼
                 Gemini LLM
                     ▼
              Answer Generator
                     ▼
              Citation Builder
                     ▼
          Hallucination Guard
                     ▼
               Final Response
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Pydantic

---

## AI

- Google Gemini
- Sentence Transformers
- all-MiniLM-L6-v2

---

## Knowledge Layer

- Neo4j
- ChromaDB

---

## Document Processing

- PyMuPDF
- python-docx
- python-pptx

---

## Security

- JWT
- Passlib
- BCrypt

---

## Deployment

- Docker
- Docker Compose

---

# Project Structure

```text
app/
│
├── api/
├── core/
├── extraction/
├── graph/
├── graphrag/
├── ingestion/
├── llm/
├── memory/
├── models/
├── ontology/
├── orchestration/
├── parsers/
├── pipelines/
├── retrieval/
├── schemas/
├── security/
├── services/
├── utils/
├── vector_store/
└── workers/

frontend/
│
├── index.html
└── static/
    ├── css/
    └── js/

tests/

docker/
```

---

# Design Principles

- Clean Architecture
- Modular Design
- Separation of Concerns
- Dependency Injection
- Service-Oriented Components
- Multi-Agent Orchestration
- Enterprise Scalability
- Explainable AI
- Retrieval-Augmented Generation
- Knowledge Graph Reasoning

---

# Installation

## Prerequisites

Before running the project, ensure the following software is installed.

- Python 3.12+
- Git
- Docker (Optional)
- Docker Compose (Optional)
- Neo4j 5+
- ChromaDB
- Google Gemini API Key

---

# Clone Repository

```bash
git clone <repository-url>

cd Enterprise_Knowledge_Assistant
```

---

# Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

# Environment Variables

Create a file named

```text
.env
```

Example

```env
# ===========================================
# Application
# ===========================================

APP_NAME=Enterprise Knowledge Assistant

ENVIRONMENT=development

DEBUG=True

HOST=0.0.0.0

PORT=8000

# ===========================================
# Gemini
# ===========================================

GEMINI_API_KEY=your_api_key

GEMINI_MODEL=gemini-2.5-flash

# ===========================================
# Neo4j
# ===========================================

NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io

NEO4J_USERNAME=neo4j

NEO4J_PASSWORD=your_password

# ===========================================
# ChromaDB
# ===========================================

CHROMA_HOST=localhost

CHROMA_PORT=8000

CHROMA_COLLECTION=enterprise_chunks

# ===========================================
# Embedding Model
# ===========================================

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# ===========================================
# JWT
# ===========================================

JWT_SECRET_KEY=replace_with_secure_secret

JWT_ALGORITHM=HS256

JWT_EXPIRE_MINUTES=60

# ===========================================
# Logging
# ===========================================

LOG_LEVEL=INFO

LOG_DIRECTORY=logs

AUDIT_LOG_PATH=logs/audit.log

# ===========================================
# Uploads
# ===========================================

UPLOAD_DIRECTORY=data/uploads
```

---

# Create Required Directories

```text
logs/

data/

data/uploads/

data/chroma/
```

---

# Running ChromaDB

If using Docker

```bash
docker run \
-p 8000:8000 \
chromadb/chroma
```

Or run your existing Chroma server.

---

# Running Neo4j

If using Neo4j Desktop

Start the database and copy

- URI
- Username
- Password

into

```
.env
```

---

# Start FastAPI

```bash
uvicorn app.main:app --reload
```

Application

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

Redoc

```
http://localhost:8000/redoc
```

---

# Frontend

Open

```
frontend/index.html
```

or serve it using a lightweight web server.

Example

```bash
python -m http.server 5500
```

Open

```
http://localhost:5500/frontend
```

---

# Docker Deployment

Build image

```bash
docker build \
-f docker/Dockerfile \
-t enterprise-knowledge-assistant .
```

Run

```bash
docker compose \
-f docker/docker-compose.yml up --build
```

Detached mode

```bash
docker compose \
-f docker/docker-compose.yml up -d
```

Stop

```bash
docker compose \
-f docker/docker-compose.yml down
```

---

# Running Tests

Run all tests

```bash
pytest
```

Integration tests

```bash
pytest tests/integration
```

End-to-End tests

```bash
pytest tests/e2e
```

Verbose

```bash
pytest -v
```

Coverage

```bash
pytest --cov=app
```

---

# Configuration

Most project settings are managed from

```
app/core/config/settings.py
```

This includes

- API configuration
- Neo4j
- ChromaDB
- Gemini
- JWT
- Logging
- Upload directory
- Embedding model

---

# Supported Document Types

Current ingestion supports

- PDF
- DOCX
- PPTX

The architecture allows additional parsers to be added without modifying the ingestion workflow.

---

# Deployment Checklist

Before deploying ensure

- Python dependencies installed
- Gemini API configured
- Neo4j running
- ChromaDB running
- Environment variables configured
- Upload directory created
- Logs directory created
- Docker containers healthy (if using Docker)
- API reachable
- Frontend connected to backend

---