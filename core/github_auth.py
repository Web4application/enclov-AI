import os, time, jwt, httpx

def create_jwt() -> str:
    with open(os.getenv("GITHUB_PRIVATE_KEY_PATH"), "r") as f:
        private_key = f.read()
    now = int(time.time())
    payload = {"iat": now, "exp": now + 600, "iss": os.getenv("GITHUB_APP_ID")}
    return jwt.encode(payload, private_key, algorithm="RS256")

async def get_installation_access_token(installation_id: int) -> str:
    jwt_token = create_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers)
        res.raise_for_status()
        return res.json()["token"]

async def post_review_comment(repo: str, pr: int, comment: str, token: str):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr}/reviews"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": comment, "event": "COMMENT"}
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=data, headers=headers)
        res.raise_for_status()
