import os
import httpx

GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
REPO = "your-username/your-repo"  # replace this
WEBHOOK_URL = "https://yourdomain.com/webhook"  # your deployed FastAPI endpoint
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

async def register_webhook():
    url = f"https://api.github.com/repos/{REPO}/hooks"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": "web",
        "active": True,
        "events": ["pull_request"],
        "config": {
            "url": WEBHOOK_URL,
            "content_type": "json",
            "secret": WEBHOOK_SECRET,
            "insecure_ssl": "0"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print("Webhook registered successfully!")
        else:
            print(f"Failed to register webhook: {response.status_code} {response.text}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(register_webhook())
