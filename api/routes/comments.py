from fastapi import APIRouter, Request, Header, HTTPException
import json
from core.security import verify_signature
from core.github_auth import get_installation_access_token
from core.ai_review import generate_ai_review_comment
import httpx

router = APIRouter()

@router.post("/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None)
):
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

            token = await get_installation_access_token(installation_id)

            async with httpx.AsyncClient() as client:
                diff_resp = await client.get(code_diff_url)
                diff_resp.raise_for_status()
                diff_text = diff_resp.text

            ai_review_comment = generate_ai_review_comment(diff_text)

            review_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json"
            }
            data = {
                "body": ai_review_comment,
                "event": "COMMENT"
            }
            async with httpx.AsyncClient() as client:
                r = await client.post(review_url, headers=headers, json=data)
                r.raise_for_status()

            return {"msg": "AI review comment posted"}

    return {"msg": "Event ignored"}
