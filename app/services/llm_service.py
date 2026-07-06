import logging

from openai import OpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate(self, user_message: str) -> str:
        if self.settings.llm_provider == "mock":
            return self._mock_generate(user_message)

        return self._openai_compatible_generate(user_message)

    def _mock_generate(self, user_message: str) -> str:
        logger.info("Using mock LLM provider")
        return f"这是 mock 模型回复：我收到了你的问题：{user_message}"

    def _openai_compatible_generate(self, user_message: str) -> str:
        if not self.settings.llm_api_key or self.settings.llm_api_key == "your_api_key_here":
            raise ValueError("LLM_API_KEY is not configured")

        client_kwargs = {
            "api_key": self.settings.llm_api_key,
        }

        if self.settings.llm_base_url:
            client_kwargs["base_url"] = self.settings.llm_base_url

        client = OpenAI(**client_kwargs)

        logger.info(
            "Calling LLM provider=%s model=%s",
            self.settings.llm_provider,
            self.settings.llm_model,
        )

        completion = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个严谨、清晰、耐心的 AI 学习助手。",
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            temperature=0.7,
        )

        content = completion.choices[0].message.content

        if content is None:
            return ""

        return content