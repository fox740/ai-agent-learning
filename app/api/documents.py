from fastapi import APIRouter, HTTPException, status

from app.models.document import DocumentListResponse, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])

document_service = DocumentService()


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