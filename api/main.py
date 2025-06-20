from fastapi import FastAPI
from api.routes.chat import router as chat_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
from app.ai_review import analyze_pr

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

class PRRequest(BaseModel):
    repo_url: str
    pr_number: int

@app.post("/api/submit")
async def submit_review(pr: PRRequest):
    try:
        result = analyze_pr(pr.repo_url, pr.pr_number)
        return JSONResponse(content={"success": True, "comments": result})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})
app = FastAPI()
app.include_router(chat_router)
