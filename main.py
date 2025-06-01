import hmac
import hashlib
import json
from fastapi import FastAPI, Header, HTTPException, Request
import httpx
import os
from api.routes import comments

app.include_router(comments.router)

app = FastAPI()

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")  # .pem file path

# You'll need PyJWT, cryptography to create JWT for GitHub App auth
import jwt
import time

def verify_signature(request_body: bytes, signature: str):
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=request_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def create_jwt():
    with open(GITHUB_PRIVATE_KEY_PATH, "r") as key_file:
        private_key = key_file.read()
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + (10 * 60),  # 10 minutes expiration
        "iss": GITHUB_APP_ID
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

async def get_installation_access_token(installation_id: int):
    jwt_token = create_jwt()
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers)
        r.raise_for_status()
        return r.json()["token"]

async def post_review_comment(repo_full_name: str, pr_number: int, body: str, token: str):
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "body": body,
        "event": "COMMENT"
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    body_bytes = await request.body()

    if not verify_signature(body_bytes, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body_bytes)

    if x_github_event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize", "reopened"]:
            pr = payload["pull_request"]
            pr_number = pr["number"]
            repo = payload["repository"]["full_name"]
            installation_id = payload["installation"]["id"]
            code_diff_url = pr["diff_url"]

            # 1. Get access token for the installation
            token = await get_installation_access_token(installation_id)

            # 2. Fetch the PR diff content (for analysis)
            async with httpx.AsyncClient() as client:
                diff_resp = await client.get(code_diff_url)
                diff_resp.raise_for_status()
                diff_text = diff_resp.text

            # 3. Here, run your AI model or API call to analyze `diff_text`
            # For demo, let's do a mock comment:
            ai_review_comment = "Hello from enclov-AI! This is a placeholder review comment."

            # 4. Post comment on PR review
            await post_review_comment(repo, pr_number, ai_review_comment, token)

            return {"msg": "Review comment posted"}

    return {"msg": "Event ignored"}
