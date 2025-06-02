from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import comments
from models.schema import CommandRequest
from enclov_commands import allowed_funcs

app = FastAPI(
    title="Enclov-AI",
    version="0.1.0",
    description="Privacy-first AI assistant for CLI + PR automation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Caution: lock this down in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

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
