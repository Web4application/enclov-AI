import hmac
import hashlib
import json
import os
import time
from fastapi import FastAPI, Header, HTTPException, Request
from urllib.parse import urlparse

import httpx
import jwt
import openai

app = FastAPI()

# Required env vars
GITHUB_WEBHOOK_SECRET = os.path.realpath("GITHUB_WEBHOOK_SECRET")
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
SAFE_ROOT_DIRECTORY = "/path/to/safe/directory"

if GITHUB_PRIVATE_KEY_PATH:
    normalized_path = os.path.realpath(GITHUB_PRIVATE_KEY_PATH)
    if not normalized_path.startswith(SAFE_ROOT_DIRECTORY):
        raise ValueError("Invalid private key path")
else:
    raise ValueError("GITHUB_PRIVATE_KEY_PATH is not set")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def verify_signature(request_body: bytes, signature: str):
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=request_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def create_jwt():
    with open(normalized_path, "r") as key_file:
        private_key = key_file.read()
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + (10 * 60),
        "iss": GITHUB_APP_ID
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

def is_valid_github_url(url: str) -> bool:
    try:
        parsed_url = urlparse(url)
        return (
            parsed_url.scheme == "https" and
            parsed_url.netloc in {"github.com", "raw.githubusercontent.com"}
        )
    except Exception:
        return False

def resolve_and_validate_ip(url: str) -> str:
    allowed_domains = {
        "github.com": "140.82.112.4",
        "raw.githubusercontent.com": "185.199.108.133"
    }
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if not hostname or hostname not in allowed_domains:
            raise ValueError("Invalid or unauthorized hostname")

        return allowed_domains[hostname]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")

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

async def analyze_diff_with_openai(diff_text: str) -> str:
    prompt = (
        "You are a meticulous AI code reviewer. Analyze this Git diff and provide a concise "
        "review with suggestions, potential bugs, style issues, and security concerns.\n\n"
        f"Diff:\n{diff_text}\n\nReview:"
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        review_text = response.choices[0].message.content.strip()
        return review_text
    except Exception as e:
        return f"AI review failed: {str(e)}"

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

            if not is_valid_github_url(code_diff_url):
                raise HTTPException(status_code=400, detail="Invalid diff URL")

            token = await get_installation_access_token(installation_id)

            validated_ip = resolve_and_validate_ip(code_diff_url)
            async with httpx.AsyncClient() as client:
                diff_resp = await client.get(f"https://{validated_ip}/diff")
                diff_resp.raise_for_status()
                diff_text = diff_resp.text

            ai_review_comment = await analyze_diff_with_openai(diff_text)

            await post_review_comment(repo, pr_number, ai_review_comment, token)

            return {"msg": "AI review comment posted"}

    return {"msg": "Event ignored"}
