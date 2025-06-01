from fastapi import APIRouter
from app.services.langchain_agent import run_agent

router = APIRouter()

@router.get("/agent")
def ask_agent(q: str):
    return {"response": run_agent(q)}
