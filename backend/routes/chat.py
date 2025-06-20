from fastapi import APIRouter, Request
from api.llm.chat_engine import run_chat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    return run_chat(user_input)
