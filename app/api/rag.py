from fastapi import APIRouter, HTTPException, status

from app.models.rag import RAGChatRequest, RAGChatResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])

rag_service = RAGService()


@router.post("/chat", response_model=RAGChatResponse)
def rag_chat(request: RAGChatRequest) -> RAGChatResponse:
    try:
        return rag_service.chat(
            question=request.question,
            top_k=request.top_k,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc