# Personalized Knowledge-Based Learning Engine

A personalized learning system that teaches a topic based on what the learner already knows.

Instead of teaching every topic from scratch, the system first identifies the prerequisites required for a topic, checks the learner's existing knowledge and study material, and then generates a personalized lesson using that knowledge.

> **Core idea:**
> **"Teach me X based on what I already know."**

---

## Features

### Personalized Learning

The learner enters a topic such as:

```text
Teach me LRU Cache
```

The system:

1. Identifies prerequisite concepts.
2. Checks what the learner already knows.
3. Separates known and unknown concepts.
4. Retrieves relevant material from the learner's uploaded notes.
5. Generates a personalized lesson.
6. Records the learning activity in study history.

---

### Knowledge-Based Learning

Learners can upload PDF study material.

The system:

```text
PDF
 ↓
Text extraction
 ↓
Cleaning & chunking
 ↓
Embeddings
 ↓
Chroma vector database
 ↓
Learner-specific knowledge
 ↓
Personalized retrieval
```

The uploaded material becomes part of the learner's personal knowledge base.

---

### Three-Agent Architecture

The system uses three LLM agents:

#### 1. Knowledge Agent

Extracts concepts and relationships from uploaded learning material.

#### 2. Requirement Agent

Determines the concepts required to understand the requested topic.

#### 3. Teaching Agent

Generates the final personalized lesson using:

* Known concepts
* Unknown concepts
* Learner's previous study material
* Retrieved context

Deterministic services handle matching, gap detection, retrieval, and study history.

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │      PDF Upload     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Parse / Clean /     │
                    │ Chunk               │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
          ┌───────────────┐        ┌────────────────┐
          │  Embeddings   │        │ Knowledge      │
          │               │        │ Extraction     │
          └───────┬───────┘        └───────┬────────┘
                  │                        │
                  ▼                        ▼
          ┌───────────────┐        ┌────────────────┐
          │    Chroma     │        │    SQLite      │
          │ Vector Store  │        │ Knowledge DB   │
          └───────┬───────┘        └───────┬────────┘
                  │                        │
                  └────────────┬───────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │  "Teach me X"     │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │ Requirement Agent │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │ Knowledge Lookup  │
                     │ & Gap Detection   │
                     └─────────┬─────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
              KNOWN                       UNKNOWN
                 │                           │
                 ▼                           ▼
       ┌─────────────────┐         ┌─────────────────┐
       │ Learner RAG     │         │ General LLM     │
       │ Retrieval       │         │ Knowledge       │
       └────────┬────────┘         └────────┬────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                     ┌───────────────────┐
                     │  Teaching Agent   │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │ Personalized      │
                     │ Lesson            │
                     └───────────────────┘
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLite
* ChromaDB
* Sentence Transformers
* PyMuPDF
* Ollama

## Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* Lucide React
* Axios

## Local LLM

The current implementation uses:

```text
llama3.2:3b
```

through Ollama.

---

# Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── documents.py
│   │   │   ├── learning.py
│   │   │   └── history.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   │
│   │   ├── embeddings/
│   │   │   └── embedder.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── document_loader.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── text_cleaner.py
│   │   │   ├── chunker.py
│   │   │   └── ingestion_service.py
│   │   │
│   │   ├── knowledge/
│   │   │   ├── knowledge_store.py
│   │   │   ├── concept_extractor.py
│   │   │   ├── knowledge_builder.py
│   │   │   └── learner_store.py
│   │   │
│   │   ├── learning/
│   │   │   ├── requirement_agent.py
│   │   │   ├── concept_matcher.py
│   │   │   ├── gap_detector.py
│   │   │   ├── learning_plan.py
│   │   │   ├── teaching_agent.py
│   │   │   └── learning_service.py
│   │   │
│   │   ├── retrieval/
│   │   │   ├── vector_store.py
│   │   │   ├── rag_service.py
│   │   │   └── learning_retriever.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── document.py
│   │   │   ├── knowledge.py
│   │   │   ├── learning.py
│   │   │   └── teaching.py
│   │   │
│   │   └── main.py
│   │
│   ├── data/
│   │   └── documents/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   ├── pages/
│   │   ├── types/
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

# Prerequisites

Install the following before running the project:

### Python

Python 3.10+ recommended.

Check:

```bash
python --version
```

or:

```bash
python3 --version
```

### Node.js

Node.js 18+ recommended.

Check:

```bash
node --version
npm --version
```

### Ollama

Install Ollama:

```text
https://ollama.com/
```

Then download the required model:

```bash
ollama pull llama3.2:3b
```

Verify:

```bash
ollama list
```

You should see:

```text
llama3.2:3b
```

Ollama should be running locally before using the learning functionality.

---

# Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

---

# Backend Setup

Open a terminal in the repository root.

```bash
cd backend
```

## Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

The default configuration is sufficient for local development.

---

# Start the Backend

From:

```text
backend/
```

run:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# Frontend Setup

Open a second terminal.

From the repository root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

## Configure frontend environment

Copy:

```text
.env.example
```

to:

```text
.env
```

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Default:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

# Start the Frontend

Run:

```bash
npm run dev
```

Vite will display the local URL, usually:

```text
http://localhost:5173
```

Open that URL in your browser.

---

# Running the Complete Application

You need three things running:

### Terminal 1 — Ollama

Ollama must be running locally with:

```text
llama3.2:3b
```

### Terminal 2 — Backend

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

### Terminal 3 — Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# First-Time Usage

## Step 1 — Create learner

The current frontend uses:

```text
LEARNER_ID = 1
```

The learner should exist in the local SQLite database.

If your project includes the learner setup script, run:

```bash
python setup_test_learner.py
```

from the backend directory.

If learner `1` already exists, no additional setup is required.

---

## Step 2 — Upload Study Material

From the Dashboard:

1. Upload a PDF containing study material.
2. Wait for processing to complete.
3. The backend will:

   * Parse the PDF.
   * Extract concepts.
   * Store learner knowledge.
   * Generate embeddings.
   * Index chunks in Chroma.
   * Record study history.

For initial testing, use a small PDF.

---

## Step 3 — Teach a Topic

Enter:

```text
LRU Cache
```

or:

```text
Linked List
```

and click:

```text
Start Learning
```

The system will determine which concepts are already known and which are new.

---

# Example Personalized Learning Flow

Suppose the learner uploaded notes containing:

```text
HashMap
Cache
Doubly Linked List
```

Then they ask:

```text
Teach me LRU Cache
```

The system may identify prerequisites such as:

```text
HashMap
Doubly Linked List
Eviction Policy
O(1) Lookup
```

The learner's existing knowledge is then matched against these requirements.

The UI distinguishes:

```text
✓ Known concept
○ New concept
🎯 Target topic
```

The Teaching Agent then generates the lesson using the learner's existing knowledge and retrieved study material.

---

# Study History & Streak

The application records learning activity using the existing history API.

Activities include:

```text
DOCUMENT_STUDIED
TOPIC_STUDIED
```

The frontend derives the study streak from real history data.

The streak represents consecutive calendar days on which the learner studied.

The dashboard also displays a study calendar showing recent activity.

No mock study data is used.

---

# API Endpoints

## Health

```http
GET /health
```

## Upload Document

```http
POST /documents/upload?learner_id={learner_id}
```

Multipart form:

```text
file=<PDF>
```

## Teach Topic

```http
POST /learning/teach
```

Request:

```json
{
  "learner_id": 1,
  "topic": "LRU Cache",
  "use_previous_material": true
}
```

## Study History

```http
GET /history/{learner_id}
```

Example:

```text
GET /history/1?limit=50
```

---

# Data Storage

The application uses local storage during development.

### SQLite

Stores:

* Learners
* Concepts
* Learner knowledge
* Concept relationships
* Study history

Location:

```text
backend/data/knowledge.db
```

### ChromaDB

Stores learner-specific vector embeddings.

Location:

```text
backend/data/chroma/
```

These generated files are intentionally excluded from Git.

Each developer creates their own local database and vector store.

---

# Troubleshooting

## Backend does not start

Make sure the virtual environment is active:

```bash
.venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Ollama connection error

Make sure Ollama is running.

Check:

```bash
ollama list
```

If the model is missing:

```bash
ollama pull llama3.2:3b
```

---

## Frontend cannot connect to backend

Verify the backend is running:

```text
http://127.0.0.1:8000/docs
```

Check:

```text
frontend/.env
```

It should contain:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Restart Vite after changing `.env`:

```bash
npm run dev
```

---

## CORS error

Make sure the backend is running with the current `main.py` configuration and restart:

```bash
uvicorn app.main:app --reload
```

The frontend normally runs on:

```text
http://localhost:5173
```

---

## No previous study material appears

Make sure:

1. A PDF was uploaded successfully.
2. The upload completed without an error.
3. The same learner ID is being used.
4. The topic has concepts that overlap with the uploaded material.

---

# Development Notes

The current project is designed as a hackathon/MVP architecture.

The core pipeline intentionally keeps:

* Agent reasoning
* Deterministic knowledge matching
* Vector retrieval
* Persistent learner state

as separate responsibilities.

Future improvements may include:

* More efficient document-level concept extraction
* Better concept normalization
* Mastery measurement
* Quiz-based knowledge verification
* More advanced retrieval/reranking
* Multi-user authentication
* Cloud deployment
* Production database
* Background document processing
* Streaming lesson generation

---

# Team Development

When contributing:

1. Pull the latest changes.

```bash
git pull
```

2. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

3. Make your changes.

4. Test both frontend and backend.

5. Commit:

```bash
git add .
git commit -m "Add your feature"
```

6. Push:

```bash
git push origin feature/your-feature
```

7. Open a Pull Request.

---

# Important

Never commit:

```text
.env
knowledge.db
Chroma data
node_modules
.venv
uploaded PDFs containing personal/private information
```

Use `.env.example` to document required environment variables.

---

# Quick Start

For experienced developers:

### Terminal 1

```bash
ollama pull llama3.2:3b
```

### Terminal 2

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### Terminal 3

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# Product Flow

```text
Upload Notes
     ↓
Build Personal Knowledge Base
     ↓
Enter "Teach Me X"
     ↓
Identify Prerequisites
     ↓
Check Existing Knowledge
     ↓
Retrieve Relevant Learner Material
     ↓
Generate Personalized Lesson
     ↓
Record Study Activity
     ↓
Update Learning History & Streak
```

## The Core Idea

> **Don't teach the learner what they already know. Use what they know to teach what they don't.**
