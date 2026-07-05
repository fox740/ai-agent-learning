from app.models.chat import ChatRequest, ChatResponse


class ChatService:
    def chat(self, request: ChatRequest) -> ChatResponse:
        reply = f"你刚才说：{request.message}"
        return ChatResponse(reply=reply)