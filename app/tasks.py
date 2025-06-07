from celery import Celery
from typing import List
from celery import shared_task
from .utils.github_client import fetch_pull_request_diff
from .utils.llm_client import analyze_code_with_llm
from .models import save_review_comments
import httpx
import os
import difflib

@shared_task
def analyze_pull_request(repo_url: str, pr_number: int):
    try:
        # 1. Fetch PR diff
        diff_text = fetch_pull_request_diff(repo_url, pr_number)
        if not diff_text:
            return {"success": False, "error": "Unable to fetch diff"}

        # 2. Use LLM to analyze PR diff
        review_comments = analyze_code_with_llm(diff_text)

        # 3. Persist and/or post comments
        save_review_comments(repo_url, pr_number, review_comments)

        return {
            "success": True,
            "comments": review_comments,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

celery_app = Celery(
    'tasks',
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.diff",
    "User-Agent": "EnclovAI-Reviewer"
}

@celery_app.task
def analyze_pull_request(repo_url: str, pr_number: int):
    """
    Fetches the PR diff, extracts code changes, and generates review comments.
    """
    try:
        owner, repo = parse_github_repo(repo_url)
        diff_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
        diff_response = httpx.get(diff_url, headers=HEADERS)

        if diff_response.status_code != 200:
            raise Exception(f"Failed to fetch PR diff: {diff_response.text}")

        diff = diff_response.text
        changes = extract_code_changes(diff)

        comments = []
        for change in changes:
            comment = analyze_code_change(change)
            if comment:
                comments.append(comment)

        return {
            "comments": comments or ["✅ No significant issues found in the pull request."]
        }

    except Exception as e:
        return {"error": str(e)}


def parse_github_repo(url: str):
    """
    Extracts the owner and repo name from the GitHub URL.
    """
    parts = url.strip("/").split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    raise ValueError("Invalid GitHub repository URL")


def extract_code_changes(diff_text: str) -> List[str]:
    """
    Parses diff and extracts hunks of code changes.
    """
    hunks = []
    current_hunk = []
    in_hunk = False

    for line in diff_text.splitlines():
        if line.startswith("@@"):
            if current_hunk:
                hunks.append("\n".join(current_hunk))
            current_hunk = [line]
            in_hunk = True
        elif in_hunk:
            current_hunk.append(line)

    if current_hunk:
        hunks.append("\n".join(current_hunk))

    return hunks


def analyze_code_change(code_hunk: str) -> str:
    """
    Analyzes a code diff hunk and returns a review comment using OpenAI.
    """
    import openai
    openai.api_key = OPENAI_API_KEY

    prompt = f"""
You are an expert code reviewer. Analyze the following Git diff hunk and suggest improvements or highlight issues:

```diff
{code_hunk}
