from pydantic import BaseModel


class ChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    char_count: int
    created_at: str


class ChunkListResponse(BaseModel):
    document_id: int
    chunks: list[ChunkResponse]
    count: int