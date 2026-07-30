# 🚀 Enterprise Knowledge Assistant (Hybrid GraphRAG + Knowledge Graph)

 **Enterprise AI Knowledge Assistant powered by Hybrid GraphRAG, Knowledge Graphs, LangGraph Multi Agent Orchestration, ChromaDB, Neo4j, FastAPI, and Google Gemini.**

An enterprise-grade AI assistant designed to transform unstructured organizational knowledge into an intelligent, searchable knowledge ecosystem. The platform combines **Vector Retrieval (RAG)**, **Knowledge Graph Retrieval**, **BM25 Keyword Search**, and **LLM-powered reasoning** to provide highly accurate, context-aware, and explainable responses for enterprise users.

------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 📖 Overview

Modern organizations generate thousands of documents including:

- Employee Handbooks
- HR Policies
- IT Security Policies
- Project Documentation
- API Documentation
- Architecture Documents
- Engineering Guidelines
- Meeting Notes
- SOPs
- Internal Knowledge Articles

Traditional keyword search cannot understand relationships between enterprise entities such as employees, departments, projects, technologies, applications, policies, and processes.

This project addresses this challenge by combining **Knowledge Graphs** with **Hybrid Retrieval-Augmented Generation (Hybrid GraphRAG)**, enabling semantic search, graph traversal, contextual reasoning, and explainable AI responses.

---

# ✨ Key Features

## 📄 Enterprise Document Ingestion

Supports ingestion of enterprise documents including:

- PDF
- DOCX
- TXT *(Extensible)*
- Markdown *(Extensible)*

Every uploaded document automatically goes through an enterprise ingestion pipeline including:

- Text Extraction
- Text Cleaning
- Language Detection
- Metadata Extraction
- Semantic Chunking
- Embedding Generation
- Vector Indexing
- BM25 Indexing
- Entity Extraction
- Relationship Extraction
- Knowledge Graph Construction

---

## 🔍 Hybrid Retrieval

Instead of relying only on vector search, the platform combines three retrieval strategies.

### 🧠 Vector Search

- ChromaDB
- Sentence Transformers
- Semantic Similarity Search

Suitable for:

- Natural language queries
- Semantic document retrieval
- Context retrieval

---

### 🕸 Knowledge Graph Search

Powered by **Neo4j**.

Retrieves:

- Entities
- Relationships
- Organizational hierarchy
- Connected enterprise knowledge

Suitable for:

- Multi-hop reasoning
- Relationship discovery
- Connected enterprise knowledge

---

### 🔎 BM25 Keyword Search

Traditional lexical retrieval for:

- Exact keywords
- Technical identifiers
- Error codes
- API names
- Policy numbers

---

# 🧩 Hybrid GraphRAG

The platform combines all retrieval sources into a unified enterprise context before passing it to the LLM.

```text
Vector Search
       │
       ▼
Knowledge Graph
       │
       ▼
BM25 Search
       │
       ▼
Context Fusion
       │
       ▼
Gemini LLM
       │
       ▼
Enterprise Response
```

---

# 🌐 Enterprise Knowledge Graph

The system automatically builds an enterprise Knowledge Graph during ingestion.

Extracted entities include:

- Organization
- Employee
- Department
- Team
- Product
- Project
- Technology
- Application
- Tool
- Policy
- Database
- API
- Process
- Location
- Infrastructure

### Example Graph

```text
TechNova Solutions
        │
        ├──────────────► HR Department
        │
        ├──────────────► IT Helpdesk
        │
        ├──────────────► Project Phoenix
        │                     │
        │                     ├────────► FastAPI
        │                     ├────────► Neo4j
        │                     ├────────► ChromaDB
        │                     ├────────► LangGraph
        │                     ├────────► Gemini
        │                     └────────► Redis
        │
        └──────────────► HR Portal
```

The graph continuously grows as additional enterprise documents are ingested.

---

# 🤖 Multi-Agent Workflow

The complete query pipeline is orchestrated using **LangGraph**, where every agent is responsible for a dedicated task.

```text
                    User Query
                         │
                         ▼
                  Router Agent
                         │
                         ▼
                Document QA Agent
                         │
                         ▼
                 Hybrid GraphRAG
                         │
                         ▼
             Answer Generation Agent
                         │
                         ▼
              Summarization Agent
                         │
                         ▼
                Citation Agent
                         │
                         ▼
               Validation Agent
                         │
                         ▼
                 Final AI Response
```

---

# 📥 End-to-End Ingestion Pipeline

Whenever a document is uploaded, the following workflow executes automatically.

```text
Upload Document
        │
        ▼
Document Parser
        │
        ▼
Text Cleaner
        │
        ▼
Language Detection
        │
        ▼
Metadata Extraction
        │
        ▼
Semantic Chunking
        │
        ▼
Embedding Generation
        │
        ▼
BM25 Index
        │
        ▼
ChromaDB Vector Store
        │
        ▼
Entity Extraction
        │
        ▼
Relationship Extraction
        │
        ▼
Entity Resolution
        │
        ▼
Knowledge Graph Construction
        │
        ▼
Neo4j
```

---

# 💬 Query Workflow

The complete enterprise query lifecycle.

```text
User Query
      │
      ▼
LangGraph Router
      │
      ▼
Hybrid Retriever
      │
      ├────────► Vector Search
      │
      ├────────► Knowledge Graph Search
      │
      └────────► BM25 Search
                    │
                    ▼
             Context Fusion
                    │
                    ▼
           Prompt Construction
                    │
                    ▼
            Google Gemini
                    │
                    ▼
         Response Generation
                    │
                    ▼
          Citation Generation
                    │
                    ▼
       Hallucination Validation
                    │
                    ▼
          Final Enterprise Answer
```

---

# ✅ Current Capabilities

- ✅ Enterprise document ingestion
- ✅ Semantic chunk generation
- ✅ Sentence Transformer embeddings
- ✅ ChromaDB vector storage
- ✅ Neo4j Knowledge Graph
- ✅ Entity extraction using Gemini
- ✅ Relationship extraction using Gemini
- ✅ Entity resolution
- ✅ Hybrid Retrieval
- ✅ GraphRAG
- ✅ LangGraph workflow orchestration
- ✅ Citation generation pipeline
- ✅ Hallucination validation
- ✅ FastAPI REST APIs
- ✅ Interactive Swagger documentation
- ✅ Modular enterprise architecture

---

# 💡 Why Hybrid GraphRAG?

Traditional RAG systems rely only on vector similarity, which may miss explicit relationships between enterprise concepts.

This project enhances retrieval by combining:

- **Semantic Search (ChromaDB)** – Finds contextually similar information.
- **Knowledge Graph (Neo4j)** – Captures entities and relationships for graph-based reasoning.
- **BM25 Retrieval** – Handles exact keyword and technical term matching.

By fusing these retrieval methods before sending context to the LLM, the assistant can generate responses that are richer, more explainable, and better aligned with enterprise knowledge than a vector-only RAG approach.

---

# 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI, Python |
| LLM | Google Gemini 2.5 Flash |
| AI Framework | LangGraph |
| Vector Database | ChromaDB |
| Graph Database | Neo4j AuraDB |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Retrieval | Hybrid (Vector + Graph + BM25) |
| Document Parsing | PDF, DOCX |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Docker, Uvicorn |

---

# 📂 Project Structure

```text
app/
├── api/
├── connectors/
├── embeddings/
├── extraction/
├── graphrag/
├── ingestion/
├── knowledge_graph/
├── llm/
├── orchestration/
├── retrieval/
├── services/
├── vector_store/
└── models/
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd Enterprise-Knowledge-Assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key

GEMINI_MODEL=gemini-2.5-flash

NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

CHROMA_DB_PATH=./data/chroma
```

---

# ▶️ Run the Project

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://localhost:8000/docs
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/v1/ingestion/upload` | Upload enterprise documents |
| POST | `/api/v1/chat` | Ask questions over enterprise knowledge |

---

# 🔄 System Workflow

## Document Ingestion

```text
Upload
   ↓
Parser
   ↓
Cleaner
   ↓
Metadata Extraction
   ↓
Semantic Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
BM25
   ↓
Entity Extraction
   ↓
Relationship Extraction
   ↓
Knowledge Graph
```

---

## Query Pipeline

```text
User Query
     ↓
Router Agent
     ↓
Hybrid Retrieval
     ├── ChromaDB
     ├── Neo4j
     └── BM25
          ↓
Context Builder
          ↓
Gemini
          ↓
Summarization
          ↓
Citation
          ↓
Validation
          ↓
Final Response
```

---

# 📈 Current Features

- Hybrid GraphRAG
- LangGraph Multi-Agent Workflow
- Enterprise Knowledge Graph
- Vector Search (ChromaDB)
- Graph Search (Neo4j)
- BM25 Keyword Retrieval
- Automatic Entity Extraction
- Automatic Relationship Extraction
- Semantic Chunking
- Citation Generation
- Hallucination Validation
- REST APIs with FastAPI

---

# 🚀 Future Enhancements

- Multi-document conversation memory
- User authentication & RBAC
- Incremental document ingestion
- Graph visualization dashboard
- Feedback-based answer improvement
- Multi-LLM support (OpenAI, Claude, Llama)
- Redis caching
- Streaming responses
- Enterprise document versioning

---

# 📸 Screenshots

Add screenshots here.

### Home Page

```
docs/screenshots/home.png
```

### Document Upload

```
docs/screenshots/upload.png
```

### Chat Interface

```
docs/screenshots/chat.png
```

### Neo4j Knowledge Graph

```
docs/screenshots/neo4j_graph.png
```

---

# 👨‍💻 Author

**Shivshankar Hatkar**
AI Engineer | L & T Technology Services

Enterprise AI | GraphRAG | LangGraph | Knowledge Graphs | Generative AI

---

# 📄 License

This project is intended for educational, research, and enterprise demonstration purposes.
