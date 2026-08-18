"""
api.py
======
PaperBrain — FastAPI application entry point.
Registers all routers, CORS, lifespan events, and health endpoints.
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import config
from backend.routes import chat, documents, history, upload
from services.cache_service import query_cache
from services.llm_service import llm_service
from services.vector_store import vector_store
from utils.logger import logger


# ─── Lifespan ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup and shutdown logic."""
    logger.info("=" * 60)
    logger.info("PaperBrain API starting up...")
    logger.info(f"LLM Provider : {config.LLM_PROVIDER} / {llm_service.model_name}")
    logger.info(f"Embedding    : {config.EMBEDDING_MODEL}")
    logger.info(f"ChromaDB     : {config.CHROMA_DIR}")
    logger.info(f"Top-K        : {config.TOP_K}")
    logger.info(f"Threshold    : {config.CONFIDENCE_THRESHOLD}")

    # Validate LLM availability at startup
    ok, msg = llm_service.is_available()
    if not ok:
        logger.warning(f"LLM not available: {msg}")
    else:
        logger.info("LLM provider: OK")

    logger.info(f"Indexed documents: {len(vector_store.get_all_documents())}")
    logger.info(f"Total chunks     : {vector_store.total_chunks()}")
    logger.info("=" * 60)

    yield  # App is running

    logger.info("PaperBrain API shutting down...")


# ─── App Factory ──────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="PaperBrain API",
        description=(
            "PaperBrain — Production-quality RAG API. "
            "Upload PDFs and ask questions answered exclusively from your documents."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(upload.router)
    app.include_router(chat.router)
    app.include_router(history.router)
    app.include_router(documents.router)

    # ── Static Files — HTML UI ────────────────────────────────────────────────
    frontend_dir = config.BASE_DIR / "frontend"
    if frontend_dir.exists():
        app.mount("/ui", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

    # ── Health / Info Endpoints ───────────────────────────────────────────────

    @app.get("/", tags=["Health"], include_in_schema=False)
    async def root():
        """Redirect root to the HTML chatbot UI."""
        return RedirectResponse(url="/ui/index.html")

    @app.get("/api", tags=["Health"])
    async def api_info() -> dict:
        return {
            "name": "PaperBrain API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs",
        }

    @app.get("/health", tags=["Health"])
    async def health() -> JSONResponse:
        """Full health check including LLM availability."""
        llm_ok, llm_msg = llm_service.is_available()
        docs = vector_store.get_all_documents()
        status_code = 200 if llm_ok else 503
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "healthy" if llm_ok else "degraded",
                "llm": {
                    "provider": llm_service.provider_name,
                    "model": llm_service.model_name,
                    "available": llm_ok,
                    "message": llm_msg,
                },
                "vector_store": {
                    "documents": len(docs),
                    "total_chunks": vector_store.total_chunks(),
                },
                "cache": query_cache.stats,
            },
        )

    @app.get("/stats", tags=["Health"])
    async def stats() -> dict:
        """Return runtime statistics."""
        return {
            "documents": len(vector_store.get_all_documents()),
            "total_chunks": vector_store.total_chunks(),
            "cache": query_cache.stats,
            "config": {
                "llm_provider": config.LLM_PROVIDER,
                "model": llm_service.model_name,
                "embedding_model": config.EMBEDDING_MODEL,
                "chunk_size": config.CHUNK_SIZE,
                "chunk_overlap": config.CHUNK_OVERLAP,
                "top_k": config.TOP_K,
                "confidence_threshold": config.CONFIDENCE_THRESHOLD,
                "hybrid_alpha": config.HYBRID_SEARCH_ALPHA,
                "rerank_enabled": config.RERANK_ENABLED,
            },
        }

    return app


# ─── Entry Point ──────────────────────────────────────────────────────────────

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level=config.LOG_LEVEL.lower(),
    )
