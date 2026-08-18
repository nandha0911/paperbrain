"""
backend/routes/documents.py
============================
GET    /documents          — List all indexed documents
DELETE /documents/{filename} — Delete a specific document
DELETE /documents          — Delete all documents
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from models.document import (
    DeleteAllResponse,
    DeleteDocumentResponse,
    DocumentListResponse,
)
from services.vector_store import vector_store
from utils.file_utils import delete_upload
from utils.logger import logger

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List all indexed documents",
)
async def list_documents() -> DocumentListResponse:
    """Return a list of all uploaded and indexed PDF documents."""
    docs = vector_store.get_all_documents()
    total_chunks = vector_store.total_chunks()
    return DocumentListResponse(
        documents=docs,
        total_documents=len(docs),
        total_chunks=total_chunks,
    )


@router.delete(
    "/{filename}",
    response_model=DeleteDocumentResponse,
    summary="Delete a specific document and its embeddings",
)
async def delete_document(filename: str) -> DeleteDocumentResponse:
    """
    Remove a document from ChromaDB and from disk.

    Args:
        filename: Exact filename of the document to remove.
    """
    doc = vector_store.get_document(filename)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{filename}' not found.",
        )

    chunks_deleted = vector_store.delete_document(filename)
    delete_upload(filename)  # remove from disk (non-fatal if missing)

    logger.info(f"Deleted document: {filename} | chunks_deleted={chunks_deleted}")
    return DeleteDocumentResponse(
        filename=filename,
        message=f"Successfully deleted '{filename}' and {chunks_deleted} chunks.",
        chunks_deleted=chunks_deleted,
    )


@router.delete(
    "",
    response_model=DeleteAllResponse,
    summary="Delete ALL documents and embeddings",
)
async def delete_all_documents() -> DeleteAllResponse:
    """
    Remove every document and all embeddings from ChromaDB.
    Also clears cached query results.
    """
    from services.cache_service import query_cache

    docs = vector_store.get_all_documents()
    filenames = [d.filename for d in docs]

    doc_count, chunk_count = vector_store.delete_all_documents()
    query_cache.invalidate()

    # Delete all files from disk
    for fname in filenames:
        delete_upload(fname)

    logger.info(f"Deleted all documents | docs={doc_count} | chunks={chunk_count}")
    return DeleteAllResponse(
        message=f"Deleted all {doc_count} documents ({chunk_count} chunks).",
        documents_deleted=doc_count,
        chunks_deleted=chunk_count,
    )
