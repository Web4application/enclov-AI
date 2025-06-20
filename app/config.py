from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import os
from urllib.parse import urlparse
import httpx
import openai

app = FastAPI()

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

def verify_signature(payload_body: bytes, signature_header: str):
    if not signature_header:
        return False
    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    body = await request.body()

    # Security first: Verify webhook signature
    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = x_github_event
    payload = await request.json()

    if event == "pull_request":
        action = payload.get("action")
        if action in ("opened", "synchronize", "reopened"):
            pr_number = payload["pull_request"]["number"]
            repo_full_name = payload["repository"]["full_name"]
            diff_url = payload["pull_request"]["diff_url"]

            # Grab the PR diff text
            async with httpx.AsyncClient() as client:
                diff_response = await client.get(diff_url, headers={"Accept": "application/vnd.github.v3.diff"})
                diff_text = diff_response.text

            # Get AI review
            review_comment = await generate_ai_review(diff_text)

            # Validate comments_url domain (trust but verify)
            comments_url = payload["pull_request"]["comments_url"]

            # Define a whitelist of allowed base URLs
            allowed_urls = [
                "https://web4application.github.io/repos/"
            ]

            # Parse and validate the comments_url
            try:
                parsed_url = urlparse(comments_url)
                if not parsed_url.scheme in ["http", "https"]:
                    raise HTTPException(status_code=400, detail="Invalid comments_url: Unsupported URL scheme")
                if not any(comments_url.startswith(allowed_url) for allowed_url in allowed_urls):
                    raise HTTPException(status_code=400, detail="Invalid comments_url: URL not in allowed whitelist")

                # Resolve domain to IP and validate against trusted range
                import socket
                resolved_ip = socket.gethostbyname(parsed_url.netloc)
                trusted_ips = ["192.30.252.0/22", "185.199.108.0/22"]  # Example GitHub IP ranges
                from ipaddress import ip_address, ip_network
                if not any(ip_address(resolved_ip) in ip_network(trusted_range) for trusted_range in trusted_ips):
                    raise HTTPException(status_code=400, detail="Invalid comments_url: IP address not in trusted range")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid comments_url: {str(e)}")

            headers = {
                "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {"body": review_comment}

            # Post comment on PR
            async with httpx.AsyncClient() as client:
                await client.post(comments_url, json=data, headers=headers)

    return {"status": "ok"}

async def generate_ai_review(diff_text: str) -> str:
    openai.api_key = OPENAI_API_KEY

    prompt = f"Review this GitHub pull request diff and provide detailed feedback:\n{diff_text}"

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content
