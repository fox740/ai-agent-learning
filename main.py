from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.upload import router as upload_router
from app.api.documents import router as documents_router
from app.api.embeddings import router as embeddings_router

setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A learning project for LLM applications and AI Agents.",
    version="0.1.0",
)

app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(embeddings_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} API",
        "env": settings.app_env,
    }