from collections.abc import Iterator
import logging
import time

from openai import OpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate(self, user_message: str) -> str:
        messages = self._build_single_turn_messages(user_message)
        return self.generate_with_messages(messages)

    def stream_generate(self, user_message: str) -> Iterator[str]:
        messages = self._build_single_turn_messages(user_message)
        yield from self.stream_generate_with_messages(messages)

    def generate_with_messages(self, messages: list[dict[str, str]]) -> str:
        if self.settings.llm_provider == "mock":
            last_user_message = self._get_last_user_message(messages)
            return self._mock_generate(last_user_message)

        return self._openai_compatible_generate(messages)

    def stream_generate_with_messages(self, messages: list[dict[str, str]]) -> Iterator[str]:
        if self.settings.llm_provider == "mock":
            last_user_message = self._get_last_user_message(messages)
            yield from self._mock_stream_generate(last_user_message)
            return

        yield from self._openai_compatible_stream_generate(messages)

    def _build_single_turn_messages(self, user_message: str) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": "你是一个严谨、清晰、耐心的 AI 学习助手。",
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

    def _get_last_user_message(self, messages: list[dict[str, str]]) -> str:
        for message in reversed(messages):
            if message["role"] == "user":
                return message["content"]

        return ""

    def _mock_generate(self, user_message: str) -> str:
        logger.info("Using mock LLM provider")
        return f"这是 mock 模型回复：我收到了你的问题：{user_message}"

    def _mock_stream_generate(self, user_message: str) -> Iterator[str]:
        logger.info("Using mock streaming LLM provider")

        text = f"这是 mock 流式回复：我收到了你的问题：{user_message}"

        for char in text:
            time.sleep(0.05)
            yield char

    def _create_client(self) -> OpenAI:
        if not self.settings.llm_api_key or self.settings.llm_api_key == "your_api_key_here":
            raise ValueError("LLM_API_KEY is not configured")

        client_kwargs = {
            "api_key": self.settings.llm_api_key,
        }

        if self.settings.llm_base_url:
            client_kwargs["base_url"] = self.settings.llm_base_url

        return OpenAI(**client_kwargs)

    def _openai_compatible_generate(self, messages: list[dict[str, str]]) -> str:
        client = self._create_client()

        logger.info(
            "Calling LLM provider=%s model=%s",
            self.settings.llm_provider,
            self.settings.llm_model,
        )

        completion = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=messages,
            temperature=0.7,
        )

        content = completion.choices[0].message.content

        if content is None:
            return ""

        return content

    def _openai_compatible_stream_generate(
        self,
        messages: list[dict[str, str]],
    ) -> Iterator[str]:
        client = self._create_client()

        logger.info(
            "Streaming LLM provider=%s model=%s",
            self.settings.llm_provider,
            self.settings.llm_model,
        )

        stream = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=messages,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta