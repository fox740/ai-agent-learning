from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to embed",
    )


class EmbeddingResponse(BaseModel):
    text: str
    embedding: list[float]
    dimension: int
    provider: str
    model: str