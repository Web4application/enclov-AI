from fastapi import FastAPI, Request, Header, HTTPException
import jwt
import time
import requests

app = FastAPI()

# GitHub App credentials
APP_ID = "YOUR_APP_ID"
PRIVATE_KEY_PATH = "path/to/private-key.pem"

# Load private key
with open(PRIVATE_KEY_PATH, "r") as key_file:
    PRIVATE_KEY = key_file.read()

def create_jwt():
    """Create a JWT for GitHub App authentication"""
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + (10 * 60),  # JWT expiration time: 10 minutes
        "iss": APP_ID
    }
    encoded_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return encoded_jwt

def get_installation_access_token(installation_id):
    """Exchange JWT for an installation access token"""
    jwt_token = create_jwt()
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    token = response.json()["token"]
    return token

@app.post("/webhook")
async def github_webhook(request: Request, x_github_event: str = Header(None)):
    payload = await request.json()

    # We only want pull_request events
    if x_github_event != "pull_request":
        return {"msg": "Event ignored"}

    action = payload.get("action")
    if action not in ["opened", "synchronize"]:
        return {"msg": f"Ignored PR action: {action}"}

    # Extract info
    pr_number = payload["number"]
    repo_owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    installation_id = payload["installation"]["id"]

    # Get access token for installation
    token = get_installation_access_token(installation_id)

    # For demo: mock AI feedback comment
    comment_body = "### enclov-AI review:\n- This is a mock review comment from enclov-AI."

    # Post comment to the PR
    comment_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post(comment_url, json={"body": comment_body}, headers=headers)
    response.raise_for_status()

    return {"msg": "Comment posted successfully"}
