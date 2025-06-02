from fastapi import FastAPI
from api.views import router as ai_router

app = FastAPI(
    title="AI Code Reviewer",
    description="An OpenAI-powered GitHub reviewer, triager, and auto-labeler.",
    version="1.0.0"
)

app.include_router(ai_router, prefix="/api")
