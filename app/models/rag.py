from pydantic import BaseModel, Field


class RAGChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User question for RAG",
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of retrieved chunks",
    )
    document_id: int | None = Field(
        default=None,
        ge=1,
        description="Optional document id filter",
    )
    min_score: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Minimum similarity score",
    )


class RAGSource(BaseModel):
    source_index: int
    chunk_id: int
    document_id: int
    filename: str
    chunk_index: int
    score: float
    content: str


class RAGChatResponse(BaseModel):
    answer: str
    sources: list[RAGSource]