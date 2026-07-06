from typing import Literal

MessageRole = Literal["user", "assistant"]


class ConversationStore:
    def __init__(self) -> None:
        self._messages: dict[str, list[dict[str, str]]] = {}

    def add_message(self, session_id: str, role: MessageRole, content: str) -> None:
        if session_id not in self._messages:
            self._messages[session_id] = []

        self._messages[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(self, session_id: str) -> list[dict[str, str]]:
        return list(self._messages.get(session_id, []))

    def clear(self, session_id: str) -> None:
        self._messages.pop(session_id, None)