from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User input message",
    )
    session_id: str = Field(
        default="default",
        min_length=1,
        max_length=100,
        description="Conversation session id",
    )


class ChatResponse(BaseModel):
    reply: str
    role: Literal["assistant"] = "assistant"
    session_id: str
    history_length: int