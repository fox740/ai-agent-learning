from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    content_type: str | None
    size: int
    preview: str