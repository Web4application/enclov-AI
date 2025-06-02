from fastapi import FastAPI, Header, HTTPException, Request
import json
from api.routes import comments
from core.security import verify_signature
from core.github_auth import get_installation_access_token
from core.ai_review import generate_ai_review_comment
import httpx
import EnclovAIPage from "./components/EnclovAIPage";
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enclov_commands import allowed_funcs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str

@app.post("/api/run")
async def run_command(req: CommandRequest):
    cmd = req.command.strip()
    func = allowed_funcs.get(cmd)

    if not func:
        return {"output": f"❌ Unknown command: '{cmd}'\nType 'enclov help' for help."}
    
    try:
        result = func()
        return {"output": result}
    except Exception as e:
        return {"output": f"🔥 Error while executing '{cmd}': {str(e)}"}

export default function Home() {
  return <EnclovAIPage />;
}

app = FastAPI(
    title="Enclov-AI",
    version="0.1.0",
    description="Privacy-first AI assistant for code reviews and PR automation."
)

# Mount all routers (API endpoints)
app.include_router(comments.router)

@app.post("/webhook")
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

            # 1. Get GitHub App token
            token = await get_installation_access_token(installation_id)

            # 2. Fetch PR diff
            async with httpx.AsyncClient() as client:
                diff_resp = await client.get(code_diff_url)
                diff_resp.raise_for_status()
                diff_text = diff_resp.text

            # 3. Generate AI review comment
            ai_review_comment = generate_ai_review_comment(diff_text)

            # 4. Post review comment
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
