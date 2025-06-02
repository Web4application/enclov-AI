from fastapi import APIRouter, Request
from pydantic import BaseModel, HttpUrl
from typing import Optional
from starlette.responses import JSONResponse
import uuid
import logging
from github import Github
from urllib.parse import urlparse

# Initialize FastAPI router
router = APIRouter()
logger = logging.getLogger(__name__)

# Replace with your GitHub Personal Access Token
GITHUB_TOKEN = "your_github_token_here"

class PRSubmission(BaseModel):
    repo_url: HttpUrl
    pr_number: int

@router.post("/api/submit")
async def submit_pr(data: PRSubmission, request: Request):
    try:
        job_id = str(uuid.uuid4())
        logger.info(f"Received PR submission: {data.repo_url} PR #{data.pr_number} [job_id={job_id}]")

        # Parse the repository URL to extract owner and repo name
        parsed_url = urlparse(str(data.repo_url))
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid repository URL format.")
        owner, repo_name = path_parts[0], path_parts[1]

        # Authenticate with GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(data.pr_number)

        # Example: Fetch pull request details
        pr_title = pr.title
        pr_body = pr.body
        pr_files = pr.get_files()
        pr_commits = pr.get_commits()

        # TODO: Implement AI review logic here
        # For demonstration, we'll create a simple review comment
        review_body = f"Automated review for PR #{data.pr_number}: Looks good overall."

        # Create a review on the pull request
        pr.create_review(body=review_body, event="COMMENT")

        return JSONResponse(content={"success": True, "job_id": job_id, "message": "Review submitted."})

    except Exception as e:
        logger.error(f"Failed to submit PR: {e}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
