import logging

from app.core.config import get_settings
from app.models.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)


class ChatService:
    def chat(self, request: ChatRequest) -> ChatResponse:
        settings = get_settings()

        logger.info("Received chat message: %s", request.message)

        reply = (
            f"你刚才说：{request.message} "
            f"当前使用模型：{settings.llm_provider}/{settings.llm_model}"
        )

        return ChatResponse(reply=reply)