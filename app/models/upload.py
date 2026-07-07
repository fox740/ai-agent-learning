from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: int
    filename: str
    content_type: str | None
    size: int
    char_count: int
    preview: str