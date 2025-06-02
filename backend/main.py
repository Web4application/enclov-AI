from fastapi import FastAPI, Request, Header, HTTPException
import hmac, hashlib, httpx
from core.env_loader import GITHUB_WEBHOOK_SECRET, GITHUB_ACCESS_TOKEN, OPENAI_API_KEY

app = FastAPI()

def verify_signature(payload_body: bytes, signature_header: str):
    if not signature_header:
        return False
    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = await request.json()
    event = x_github_event

    if event == "pull_request":
        action = payload.get("action")
        if action in ("opened", "synchronize", "reopened"):
            pr_number = payload["pull_request"]["number"]
            repo_full_name = payload["repository"]["full_name"]
            diff_url = payload["pull_request"]["diff_url"]

            async with httpx.AsyncClient() as client:
                diff_response = await client.get(diff_url, headers={"Accept": "application/vnd.github.v3.diff"})
                diff_text = diff_response.text

            review_comment = await generate_ai_review(diff_text)

            comments_url = payload["pull_request"]["comments_url"]
            headers = {
                "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {"body": review_comment}

            async with httpx.AsyncClient() as client:
                await client.post(comments_url, json=data, headers=headers)

    return {"status": "ok"}

async def generate_ai_review(diff_text: str) -> str:
    import openai
    openai.api_key = OPENAI_API_KEY

    prompt = f"Review this GitHub pull request diff and provide detailed feedback:\n{diff_text}"

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content
