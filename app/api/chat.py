from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chat", tags=["chat"])

chat_service = ChatService()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return chat_service.chat(request)


@router.post("/stream")
def stream_chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        chat_service.stream_chat(request),
        media_type="text/plain; charset=utf-8",
    )