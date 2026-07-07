from fastapi import APIRouter, HTTPException, Query, status

from app.models.chunk import ChunkListResponse
from app.models.document import DocumentListResponse, DocumentResponse
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])

document_service = DocumentService()
chunk_service = ChunkService()


@router.get("", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    documents = document_service.list_documents()

    return DocumentListResponse(
        documents=documents,
        count=len(documents),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int) -> DocumentResponse:
    document = document_service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.post("/{document_id}/chunks", response_model=ChunkListResponse)
def create_document_chunks(
    document_id: int,
    chunk_size: int = Query(default=500, ge=100, le=5000),
    chunk_overlap: int = Query(default=100, ge=0, le=1000),
) -> ChunkListResponse:
    document = document_service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    try:
        chunks = chunk_service.create_chunks(
            document=document,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ChunkListResponse(
        document_id=document_id,
        chunks=chunks,
        count=len(chunks),
    )


@router.get("/{document_id}/chunks", response_model=ChunkListResponse)
def get_document_chunks(document_id: int) -> ChunkListResponse:
    document = document_service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    chunks = chunk_service.get_chunks(document_id)

    return ChunkListResponse(
        document_id=document_id,
        chunks=chunks,
        count=len(chunks),
    )