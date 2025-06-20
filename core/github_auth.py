import os
import time
import httpx
import jwt  # PyJWT
from cryptography.hazmat.primitives import serialization

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")

def create_jwt() -> str:
    with open(GITHUB_PRIVATE_KEY_PATH, "r") as key_file:
        private_key = key_file.read()

    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + (10 * 60),
        "iss": GITHUB_APP_ID
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

async def get_installation_access_token(installation_id: int) -> str:
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
