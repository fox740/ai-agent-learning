from pydantic import BaseModel


class DocumentIndexResponse(BaseModel):
    document_id: int
    status: str
    chunk_count: int
    embedding_count: int
    chunk_size: int
    chunk_overlap: int