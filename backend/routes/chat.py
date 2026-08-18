"""
backend/routes/chat.py
======================
POST /chat       — Synchronous chat endpoint
POST /chat/stream — Server-Sent Events streaming endpoint
"""

from __future__ import annotations

import json
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from models.chat import ChatRequest, ChatResponse
from services.rag_service import rag_service
from utils.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send a question and receive a full answer",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a question against uploaded documents using the RAG pipeline.

    - Retrieves top-K relevant chunks from ChromaDB.
    - Applies confidence threshold filtering.
    - Constructs prompt and calls the configured LLM.
    - Returns answer with source citations and confidence score.
    """
    try:
        response = rag_service.chat(request)
        return response
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}",
        )


@router.post(
    "/stream",
    summary="Stream a chat response via Server-Sent Events",
    response_class=StreamingResponse,
)
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """
    Stream a chat response token-by-token using SSE.

    Each SSE event is a JSON payload with one of:
      {"type": "token", "content": "..."}
      {"type": "sources", "sources": [...]}
      {"type": "done", "confidence": 0.xx, "processing_time_ms": N}
      {"type": "error", "detail": "..."}
    """
    async def event_generator() -> AsyncIterator[str]:
        try:
            for event in rag_service.chat_stream(request):
                data = json.dumps(event, default=str)
                yield f"data: {data}\n\n"
        except Exception as e:
            logger.error(f"Stream error: {e}")
            error_data = json.dumps({"type": "error", "detail": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
