from openai import OpenAI

from app.core.config import get_settings


class EmbeddingService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def embed_text(self, text: str) -> list[float]:
        if self.settings.embedding_provider != "dashscope":
            raise ValueError(
                f"Unsupported embedding provider: {self.settings.embedding_provider}"
            )

        return self._dashscope_embed_text(text)

    def _create_client(self) -> OpenAI:
        if (
            not self.settings.embedding_api_key
            or self.settings.embedding_api_key == "your_dashscope_api_key_here"
        ):
            raise ValueError("EMBEDDING_API_KEY is not configured")

        return OpenAI(
            api_key=self.settings.embedding_api_key,
            base_url=self.settings.embedding_base_url,
        )

    def _dashscope_embed_text(self, text: str) -> list[float]:
        client = self._create_client()

        response = client.embeddings.create(
            model=self.settings.embedding_model,
            input=text,
            dimensions=self.settings.embedding_dim,
        )

        embedding = response.data[0].embedding

        return list(embedding)