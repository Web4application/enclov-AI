import os
from fastapi import APIRouter, HTTPException, Query
from github import Github
from utils import github_inline, triage
import openai

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

if not OPENAI_API_KEY or not GITHUB_TOKEN or not REPO_NAME:
    raise RuntimeError("Missing required environment variables.")

openai.api_key = OPENAI_API_KEY
gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(REPO_NAME)


@router.get("/review")
async def review_pull_request(pr_number: int = Query(..., description="Pull Request number")):
    try:
        pr = repo.get_pull(pr_number)
        github_inline.add_inline_review_comments(pr, gh, OPENAI_API_KEY)

        files_changed = [f.filename for f in pr.get_files()]
        ai_response = triage.analyze_pr_with_openai(pr.title, pr.body or "", files_changed)
        summary, labels = triage.extract_labels_from_ai(ai_response)

        if summary:
            pr.create_issue_comment(f"🧠 **AI Summary:**\n\n{summary}")
        if labels:
            pr.add_to_labels(*labels)

        reviewers = triage.match_reviewers_by_paths(files_changed)
        if reviewers:
            pr.create_review_request(reviewers=reviewers)

        return {"status": "success", "summary": summary, "labels": labels, "reviewers": reviewers}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
