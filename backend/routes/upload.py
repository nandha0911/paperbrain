"""
backend/routes/upload.py
========================
POST /upload — PDF upload, validation, processing, and indexing.
"""

from __future__ import annotations

import time
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

import config
from models.document import DocumentInfo, ProcessingStatus, UploadResponse
from services.pdf_service import pdf_service
from services.vector_store import vector_store
from utils.file_utils import (
    delete_upload,
    get_upload_path,
    sanitize_filename,
    validate_pdf_bytes,
)
from utils.hash_utils import compute_file_hash
from utils.logger import logger

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and index a PDF file",
)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload a PDF file, extract text, embed chunks, and store in ChromaDB.

    - Validates file type and size.
    - Detects duplicate uploads via SHA-256 hash.
    - Extracts text (with OCR fallback for scanned PDFs).
    - Chunks text and stores embeddings in ChromaDB.
    """
    start_time = time.time()

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided.",
        )

    # ── Read bytes ────────────────────────────────────────────────────────────
    file_bytes = await file.read()

    # ── Validate ──────────────────────────────────────────────────────────────
    safe_name = sanitize_filename(file.filename)
    is_valid, error_msg = validate_pdf_bytes(file_bytes, safe_name)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_msg,
        )

    # ── Duplicate check ───────────────────────────────────────────────────────
    file_hash = compute_file_hash(file_bytes)
    existing_filename = vector_store.document_exists(file_hash)
    if existing_filename:
        logger.info(f"Duplicate upload detected: {safe_name} == {existing_filename}")
        existing_info = vector_store.get_document(existing_filename)
        return UploadResponse(
            filename=existing_filename,
            file_hash=file_hash,
            file_size_bytes=len(file_bytes),
            page_count=existing_info.page_count if existing_info else 0,
            chunk_count=existing_info.chunk_count if existing_info else 0,
            status=ProcessingStatus.COMPLETED,
            message=f"Duplicate document. Already indexed as '{existing_filename}'.",
            already_exists=True,
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    # ── Check max files ───────────────────────────────────────────────────────
    current_docs = vector_store.get_all_documents()
    if len(current_docs) >= config.MAX_FILES_PER_SESSION:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Maximum number of documents ({config.MAX_FILES_PER_SESSION}) reached. "
                "Delete some documents before uploading new ones."
            ),
        )

    # ── Save to disk ──────────────────────────────────────────────────────────
    save_path = get_upload_path(safe_name)
    # Handle filename collisions (same name, different content)
    if save_path.exists():
        stem = Path(safe_name).stem
        ext = Path(safe_name).suffix
        safe_name = f"{stem}_{file_hash[:6]}{ext}"
        save_path = get_upload_path(safe_name)

    save_path.write_bytes(file_bytes)
    logger.info(f"Saved PDF to disk: {save_path}")

    # ── Process (extract → clean → chunk) ────────────────────────────────────
    try:
        chunks, page_count, _ = pdf_service.process_pdf(file_bytes, safe_name)
    except Exception as e:
        save_path.unlink(missing_ok=True)
        logger.error(f"PDF processing failed for {safe_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process PDF: {str(e)}",
        )

    if not chunks:
        save_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No extractable text found in the PDF. "
                   "The file may be image-only and OCR is required.",
        )

    # ── Index in ChromaDB ─────────────────────────────────────────────────────
    doc_info = DocumentInfo(
        filename=safe_name,
        file_hash=file_hash,
        file_size_bytes=len(file_bytes),
        page_count=page_count,
        chunk_count=len(chunks),
        status=ProcessingStatus.PROCESSING,
    )

    try:
        stored_count = vector_store.add_chunks(chunks, doc_info)
        doc_info.status = ProcessingStatus.COMPLETED
        doc_info.chunk_count = stored_count
    except Exception as e:
        save_path.unlink(missing_ok=True)
        logger.error(f"Vector store indexing failed for {safe_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index document: {str(e)}",
        )

    processing_ms = int((time.time() - start_time) * 1000)
    logger.info(
        f"Upload complete: {safe_name} | pages={page_count} | "
        f"chunks={stored_count} | time={processing_ms}ms"
    )

    return UploadResponse(
        filename=safe_name,
        file_hash=file_hash,
        file_size_bytes=len(file_bytes),
        page_count=page_count,
        chunk_count=stored_count,
        status=ProcessingStatus.COMPLETED,
        message=f"Successfully indexed '{safe_name}' — {stored_count} chunks from {page_count} pages.",
        already_exists=False,
        processing_time_ms=processing_ms,
    )
