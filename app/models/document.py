from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    content_type: str | None
    size: int
    char_count: int
    created_at: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    count: int