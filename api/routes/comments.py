from fastapi import APIRouter, Request, Header, HTTPException
from core.security import verify_signature
from core.github_auth import get_installation_access_token, post_review_comment
from core.ai_review import generate_ai_review
import json
import httpx

router = APIRouter()

@router.post("/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body)

    if x_github_event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize", "reopened"]:
            pr = payload["pull_request"]
            repo = payload["repository"]["full_name"]
            pr_number = pr["number"]
            installation_id = payload["installation"]["id"]
            diff_url = pr["diff_url"]

            token = await get_installation_access_token(installation_id)

            async with httpx.AsyncClient() as client:
                r = await client.get(diff_url)
                diff = r.text

            review = await generate_ai_review(diff)
            await post_review_comment(repo, pr_number, review, token)

            return {"msg": "AI review posted"}

    return {"msg": "Event ignored"}
    from fastapi import APIRouter, Body

router = APIRouter(prefix="/comments", tags=["AI Review"])

@router.post("/analyze")
async def analyze_code_diff(diff: str = Body(..., embed=True)):
    # This is a stub for direct diff input (non-GitHub use)
    from core.ai_review import generate_ai_review_comment
    return {"comment": generate_ai_review_comment(diff)}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

async function fetchComments(jobId: string) {
  const res = await fetch(`${API_BASE_URL}/api/comments?job_id=${jobId}`);
  const data = await res.json();
  return data;
}

