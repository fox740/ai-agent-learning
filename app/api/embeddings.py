from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.models.embedding import EmbeddingRequest, EmbeddingResponse
from app.services.embedding_service import EmbeddingService


router = APIRouter(prefix="/embeddings", tags=["embeddings"])

settings = get_settings()
embedding_service = EmbeddingService()


@router.post("", response_model=EmbeddingResponse)
def create_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    try:
        embedding = embedding_service.embed_text(request.text)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return EmbeddingResponse(
        text=request.text,
        embedding=embedding,
        dimension=len(embedding),
        provider=settings.embedding_provider,
        model=settings.embedding_model,
    )