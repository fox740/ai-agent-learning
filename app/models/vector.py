from pydantic import BaseModel


class ChunkEmbeddingResponse(BaseModel):
    id: int
    chunk_id: int
    document_id: int
    embedding: list[float]
    dimension: int
    created_at: str


class ChunkEmbeddingListResponse(BaseModel):
    document_id: int
    embeddings: list[ChunkEmbeddingResponse]
    count: int