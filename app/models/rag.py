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


class RAGSource(BaseModel):
    chunk_id: int
    document_id: int
    chunk_index: int
    score: float
    content: str


class RAGChatResponse(BaseModel):
    answer: str
    sources: list[RAGSource]