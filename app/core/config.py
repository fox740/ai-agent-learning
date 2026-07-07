from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="AI Agent Learning", alias="APP_NAME")
    app_env: Literal["development", "testing", "production"] = Field(
        default="development",
        alias="APP_ENV",
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    llm_provider: Literal["mock", "openai", "deepseek", "qwen"] = Field(
        default="mock",
        alias="LLM_PROVIDER",
    )
    llm_model: str = Field(default="mock-chat-model", alias="LLM_MODEL")
    llm_base_url: str = Field(default="", alias="LLM_BASE_URL")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    prompt_name: str = Field(default="default", alias="PROMPT_NAME")

    embedding_provider: str = Field(default="dashscope", alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="text-embedding-v4", alias="EMBEDDING_MODEL")
    embedding_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        alias="EMBEDDING_BASE_URL",
    )
    embedding_api_key: str = Field(default="", alias="EMBEDDING_API_KEY")
    embedding_dim: int = Field(default=1024, alias="EMBEDDING_DIM")
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()