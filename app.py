from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import comments
from models.schema import CommandRequest
from enclov_commands import allowed_funcs
from app.routes import submit_pr  # adjust path as needed
from fastapi import FastAPI
from submit_pr import router as submit_pr_router
from providers.enclovai_provider import call_enclovai

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_prompt(prompt, model="auto"):
    return call_enclovai(prompt, model=model)

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    provider = input("Choose provider (openai/google/auto): ").strip().lower()
    response = process_prompt(prompt, model=provider)
    print("\n=== Response ===\n")
    print(response)

app = FastAPI(
    title="Enclov-AI",
    version="0.1.0",
    description="Privacy-first AI assistant for CLI + PR automation"
)

app = FastAPI()
app.include_router(submit_pr_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Caution: lock this down in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(submit_pr.router)

# CLI command endpoint
@app.post("/api/run")
async def run_command(req: CommandRequest):
    cmd = req.command.strip()
    func = allowed_funcs.get(cmd)

    if not func:
        return {"output": f"❌ Unknown command: '{cmd}'\nType 'enclov help' for help."}
    
    try:
        return {"output": func()}
    except Exception as e:
        return {"output": f"🔥 Error while executing '{cmd}': {str(e)}"}

# GitHub Webhook endpoint
app.include_router(comments.router)
