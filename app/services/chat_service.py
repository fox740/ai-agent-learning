from collections.abc import Iterator
import logging

from app.models.chat import ChatRequest, ChatResponse
from app.services.conversation_store import ConversationStore
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self) -> None:
        self.llm_service = LLMService()
        self.conversation_store = ConversationStore()

    def chat(self, request: ChatRequest) -> ChatResponse:
        logger.info(
            "Received chat message session_id=%s message=%s",
            request.session_id,
            request.message,
        )

        self.conversation_store.add_message(
            session_id=request.session_id,
            role="user",
            content=request.message,
        )

        history = self.conversation_store.get_messages(request.session_id)
        messages = self._build_messages(history)

        reply = self.llm_service.generate_with_messages(messages)

        self.conversation_store.add_message(
            session_id=request.session_id,
            role="assistant",
            content=reply,
        )

        history_length = len(self.conversation_store.get_messages(request.session_id))

        return ChatResponse(
            reply=reply,
            session_id=request.session_id,
            history_length=history_length,
        )

    def stream_chat(self, request: ChatRequest) -> Iterator[str]:
        logger.info(
            "Received streaming chat message session_id=%s message=%s",
            request.session_id,
            request.message,
        )

        self.conversation_store.add_message(
            session_id=request.session_id,
            role="user",
            content=request.message,
        )

        history = self.conversation_store.get_messages(request.session_id)
        messages = self._build_messages(history)

        full_reply = ""

        for chunk in self.llm_service.stream_generate_with_messages(messages):
            full_reply += chunk
            yield chunk

        self.conversation_store.add_message(
            session_id=request.session_id,
            role="assistant",
            content=full_reply,
        )

    def _build_messages(self, history: list[dict[str, str]]) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": "你是一个严谨、清晰、耐心的 AI 学习助手。",
            },
            *history,
        ]