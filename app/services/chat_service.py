import logging

from app.models.chat import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from collections.abc import Iterator

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self) -> None:
        self.llm_service = LLMService()

    def chat(self, request: ChatRequest) -> ChatResponse:
        logger.info("Received chat message: %s", request.message)

        reply = self.llm_service.generate(request.message)

        return ChatResponse(reply=reply)
    
    def stream_chat(self, request: ChatRequest) -> Iterator[str]:
        logger.info("Received streaming chat message: %s", request.message)

        return self.llm_service.stream_generate(request.message)