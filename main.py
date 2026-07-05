from fastapi import FastAPI

from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Agent Learning",
    description="A learning project for LLM applications and AI Agents.",
    version="0.1.0",
)

app.include_router(chat_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Agent Learning API"}