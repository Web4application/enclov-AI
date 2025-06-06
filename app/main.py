from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.tasks import analyze_pull_request
import os

app = FastAPI()

class PRRequest(BaseModel):
    repo_url: str
    pr_number: int

@app.post("/api/submit")
async def submit_pr(pr: PRRequest):
    task = analyze_pull_request.delay(pr.repo_url, pr.pr_number)
    return {"job_id": task.id}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    task_result = AsyncResult(job_id)
    if task_result.state == 'PENDING':
        return {"status": "pending"}
    elif task_result.state == 'SUCCESS':
        return {"status": "completed", "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": "failed", "error": str(task_result.result)}
    else:
        return {"status": task_result.state}
