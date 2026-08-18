# PaperBrain 🧠

A **production-quality** Retrieval-Augmented Generation (RAG) chatbot that answers questions **exclusively** from uploaded PDF documents. Powered by **Ollama** (local LLM), **ChromaDB** (vector database), and **BAAI/bge-small-en-v1.5** embeddings.

> *Your papers. Your answers. Nothing else.*
---

## ✨ Features

| Feature | Details |
|---|---|
| 📤 Multi-PDF Upload | Upload 1–20 PDFs, view, and delete them |
| 🔍 Hybrid Search | Vector similarity + BM25 keyword search fused via RRF |
| 🧠 Cross-Encoder Reranking | `ms-marco-MiniLM` reranks top candidates for precision |
| 💬 Conversation Memory | Last 10 turns, context-aware follow-up questions |
| 📎 Source Citations | Every answer shows PDF name, page number, and snippet |
| 📊 Confidence Score | Visual bar; rejects answers below 0.40 threshold |
| ⚡ Query Caching | LRU+TTL cache avoids duplicate LLM calls |
| 🔒 No Hallucinations | ONLY answers from uploaded documents |
| 🌙 Dark Mode UI | Premium glassmorphism Streamlit interface |
| 🔌 Pluggable LLM | Switch between Ollama / OpenAI / Gemini via `.env` |
| 🗺️ OCR Support | Falls back to Tesseract for scanned PDFs |
| 🛡️ Security | File validation, sanitisation, size limits, hash dedup |

---

## 🏗️ Architecture

```
Streamlit UI  →  FastAPI Backend  →  RAG Service
                                         │
                    PDF Service    Embedding Service    LLM Service (Ollama)
                         │                │
                    ChromaDB (Vector Store)
```

---

## 📁 Project Structure

```
rag-chatbot/
├── app.py                   # Streamlit frontend
├── api.py                   # FastAPI backend
├── config.py                # All configuration
├── requirements.txt
├── .env.example
│
├── models/                  # Pydantic data schemas
│   ├── chat.py
│   └── document.py
│
├── services/                # Core business logic
│   ├── pdf_service.py       # Extract · Clean · Chunk
│   ├── embedding_service.py # Sentence Transformer (BGE)
│   ├── vector_store.py      # ChromaDB + BM25 + Reranker
│   ├── llm_service.py       # Ollama / OpenAI / Gemini
│   ├── rag_service.py       # Full pipeline orchestrator
│   └── cache_service.py     # LRU+TTL query cache
│
├── prompts/
│   └── templates.py         # All prompt templates
│
├── utils/
│   ├── logger.py            # Loguru structured logging
│   ├── file_utils.py        # Validation & sanitisation
│   ├── text_utils.py        # Text cleaning helpers
│   └── hash_utils.py        # SHA-256 dedup
│
├── backend/routes/
│   ├── upload.py            # POST /upload
│   ├── chat.py              # POST /chat, POST /chat/stream
│   ├── history.py           # GET/DELETE /history/{id}
│   └── documents.py         # GET/DELETE /documents
│
├── frontend/
│   ├── components.py        # Reusable Streamlit components
│   └── styles.py            # Custom dark-mode CSS
│
├── uploads/                 # Saved PDFs (auto-created)
├── chroma_db/               # ChromaDB persistent store (auto-created)
├── data/                    # Misc data (auto-created)
└── logs/                    # Log files (auto-created)
```

---

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- (Optional) Tesseract OCR for scanned PDFs

### 2. Install Ollama & Pull a Model

```bash
# Install Ollama from https://ollama.com
# Then pull the default model:
ollama pull llama3
```

### 3. Clone & Setup

```bash
# Navigate to project directory
cd rag-chatbot

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example env file
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# Edit .env if needed (defaults work with Ollama + llama3)
```

### 5. Start the FastAPI Backend

```bash
python api.py
# API running at http://127.0.0.1:8000
# Docs at      http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit Frontend

Open a **new terminal** (keep the backend running):

```bash
streamlit run app.py
# UI at http://localhost:8501
```

---

## 🔧 Configuration

All settings are in `.env` (copy from `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | `ollama` / `openai` / `gemini` |
| `OLLAMA_MODEL` | `llama3` | Any Ollama model (e.g. `mistral`, `phi3`) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | Sentence Transformer model |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `TOP_K` | `5` | Chunks retrieved per query |
| `CONFIDENCE_THRESHOLD` | `0.40` | Minimum similarity score |
| `RERANK_ENABLED` | `true` | Cross-encoder reranking |
| `HYBRID_SEARCH_ALPHA` | `0.7` | Weight for vector vs. keyword (1.0 = pure vector) |
| `MAX_FILE_SIZE_MB` | `50` | Max upload size |

---

## 🔌 Switching LLM Provider

### Use Mistral instead of Llama 3

```env
OLLAMA_MODEL=mistral
```
```bash
ollama pull mistral
```

### Use OpenAI GPT-4o

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```
```bash
pip install openai
```

### Use Google Gemini

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-1.5-flash
```
```bash
pip install google-generativeai
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload` | Upload & index a PDF |
| `POST` | `/chat` | Ask a question (sync) |
| `POST` | `/chat/stream` | Ask a question (SSE stream) |
| `GET` | `/documents` | List all indexed documents |
| `DELETE` | `/documents/{filename}` | Delete a specific document |
| `DELETE` | `/documents` | Delete ALL documents |
| `GET` | `/history/{session_id}` | Get conversation history |
| `DELETE` | `/history/{session_id}` | Clear conversation history |
| `GET` | `/health` | Health check (LLM + vector store) |
| `GET` | `/stats` | Runtime statistics |

Interactive docs: **http://127.0.0.1:8000/docs**

---

## 📊 RAG Pipeline

```
User Question
     │
     ▼
Question Rephrasing (if follow-up with pronouns)
     │
     ▼
Hybrid Search ──── Vector Search (ChromaDB cosine)
     │         └── BM25 Keyword Search
     │              └── Reciprocal Rank Fusion
     ▼
Cross-Encoder Reranking (ms-marco-MiniLM)
     │
     ▼
Confidence Filter (≥ 0.40)
     │
     ▼
Prompt Construction  ← Context + History + Question
     │
     ▼
Ollama LLM Generation
     │
     ▼
Answer + Source Citations + Confidence Score
```

---

## 🛡️ Security Features

- **File validation** — PDF magic bytes check + extension check
- **Size limit** — 50 MB max per file (configurable)
- **Filename sanitisation** — prevents path traversal
- **Duplicate detection** — SHA-256 hash comparison
- **Max files** — 20 PDFs per session (configurable)
- **No external calls** — fully local with Ollama

---

## 🧪 OCR for Scanned PDFs

Install dependencies:

```bash
# Windows
# 1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# 2. Add to PATH
# 3. Install poppler: https://github.com/oschwartz10612/poppler-windows/releases

pip install pytesseract pdf2image Pillow
```

OCR is automatically triggered when a page has < 30 characters of native text.

---

## 📝 Logs

Logs are stored in `logs/rag_chatbot.log` with 10MB rotation and 7-day retention.

```bash
# View live logs
tail -f logs/rag_chatbot.log       # macOS/Linux
Get-Content logs/rag_chatbot.log -Wait  # Windows PowerShell
```

---

## 🚀 Performance Tips

1. **GPU acceleration** — set `EMBEDDING_DEVICE=cuda` if you have a GPU
2. **Faster model** — use `phi3:mini` or `gemma2:2b` for speed over quality
3. **Larger Top-K** — increase `TOP_K` for better recall at cost of latency
4. **Cache** — enable `CACHE_ENABLED=true` (default) to skip repeat queries
5. **Disable reranking** — set `RERANK_ENABLED=false` for lower latency

---

## 📌 Troubleshooting

| Problem | Fix |
|---|---|
| `Cannot reach API` | Run `python api.py` first |
| `LLM Offline` | Run `ollama serve` and `ollama pull llama3` |
| `No text extracted` | Enable OCR (see above) or try a different PDF |
| `Slow responses` | Use a smaller Ollama model like `phi3:mini` |
| `Import errors` | Activate venv: `venv\Scripts\activate` |

---

## 📄 License

MIT License — free to use, modify, and distribute.
