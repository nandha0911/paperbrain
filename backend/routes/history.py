"""
backend/routes/history.py
=========================
GET  /history/{session_id}    — Retrieve conversation history
DELETE /history/{session_id}  — Clear conversation history
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from models.chat import ClearHistoryResponse, HistoryResponse
from services.rag_service import rag_service
from utils.logger import logger

router = APIRouter(prefix="/history", tags=["History"])


@router.get(
    "/{session_id}",
    response_model=HistoryResponse,
    summary="Get conversation history for a session",
)
async def get_history(session_id: str) -> HistoryResponse:
    """Return all messages in a conversation session."""
    messages = rag_service.get_history(session_id)
    return HistoryResponse(
        session_id=session_id,
        messages=messages,
        total_messages=len(messages),
    )


@router.delete(
    "/{session_id}",
    response_model=ClearHistoryResponse,
    summary="Clear conversation history for a session",
)
async def clear_history(session_id: str) -> ClearHistoryResponse:
    """Delete all messages in a conversation session."""
    cleared = rag_service.clear_history(session_id)
    logger.info(f"Cleared {cleared} messages for session {session_id}")
    return ClearHistoryResponse(
        session_id=session_id,
        message=f"Cleared {cleared} messages from session '{session_id}'.",
        cleared_count=cleared,
    )
