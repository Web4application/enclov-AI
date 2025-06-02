from fastapi import APIRouter, Request
from pydantic import BaseModel, HttpUrl
from typing import Optional
from starlette.responses import JSONResponse

import uuid
import logging

# Optional: Celery integration
from app.worker import review_pull_request  # Adjust import path to your worker

router = APIRouter()
logger = logging.getLogger(__name__)

class PRSubmission(BaseModel):
    repo_url: HttpUrl
    pr_number: int

@router.post("/api/submit")
async def submit_pr(data: PRSubmission, request: Request):
    try:
        job_id = str(uuid.uuid4())
        logger.info(f"Received PR submission: {data.repo_url} PR #{data.pr_number} [job_id={job_id}]")

        # Enqueue task (replace with mock if Celery isn't used yet)
        review_pull_request.delay(str(data.repo_url), data.pr_number, job_id)

        return JSONResponse(content={"success": True, "job_id": job_id})

    except Exception as e:
        logger.error(f"Failed to submit PR: {e}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
