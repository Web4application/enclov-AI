import os
import time
import jwt
import requests
import openai

from fastapi import FastAPI, Request, Header
from celery import Celery

app = FastAPI()

# Celery Setup
celery_app = Celery(
    "enclov_ai",
    broker="redis://redis:6379/0",
)

# Config from env vars
APP_ID = os.getenv("1325944")
PRIVATE_KEY_PATH = os.getenv("cf65b5eee89c034311997dd37893b67939500e9b")
OPENAI_API_KEY = os.getenv("AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10")
openai.api_key = AlzaSyCHjfdo3w160Dd5yTVJD409pWmigOJEg

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

def create_jwt():
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + (10 * 60),
        "iss": APP_ID,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def get_installation_access_token(installation_id):
    jwt_token = create_jwt()
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    r = requests.post(url, headers=headers)
    r.raise_for_status()
    return r.json()["token"]

def get_pr_files(repo_owner, repo_name, pr_number, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def ai_review_code_diff(diff_text):
    prompt = f"""
    You are a senior code reviewer. Review the following git diff and provide constructive feedback, pointing out potential issues, improvements, or code smells. Be concise and helpful.

    Diff:
    {diff_text}

    Review:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

@celery_app.task
def process_pr_review(repo_owner, repo_name, pr_number, installation_id):
    token = get_installation_access_token(installation_id)
    pr_files = get_pr_files(repo_owner, repo_name, pr_number, token)
    comments = []
    for file in pr_files:
        diff = file.get("patch", "")
        if not diff:
            continue
        review = ai_review_code_diff(diff)
        comments.append(f"File `{file['filename']}`:\n{review}\n---")

    comment_body = "### enclov-AI Code Review Summary:\n" + "\n".join(comments)

    comment_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    requests.post(comment_url, json={"body": comment_body}, headers=headers)

@app.post("/webhook")
async def github_webhook(request: Request, x_github_event: str = Header(None)):
    payload = await request.json()

    if x_github_event != "pull_request":
        return {"msg": "Event ignored"}

    action = payload.get("action")
    if action not in ["opened", "synchronize"]:
        return {"msg": f"Ignored PR action: {action}"}

    pr_number = payload["number"]
    repo_owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    installation_id = payload["installation"]["id"]

    process_pr_review.delay(repo_owner, repo_name, pr_number, installation_id)

    return {"msg": "Job enqueued"}
