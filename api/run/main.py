# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import shlex

app = FastAPI()

# Allow frontend to talk to backend (adjust origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str

@app.post("/api/run")
async def run_command(req: CommandRequest):
    cmd = req.command.strip()

    # ✋ Simple allowlist to avoid arbitrary execution
    allowed_cmds = {
        "enclov version": "echo 'Enclov CLI v1.0.2'",
        "enclov config": "echo '{\"env\": \"production\", \"autosync\": true}'",
        "enclov start": "echo 'Starting Enclov Engine... Ready ✅'",
    }

    if cmd not in allowed_cmds:
        return {"output": f"❌ Unknown or disallowed command: {cmd}"}

    try:
        result = subprocess.check_output(
            shlex.split(allowed_cmds[cmd]),
            stderr=subprocess.STDOUT,
            text=True
        )
        return {"output": result}
    except subprocess.CalledProcessError as e:
        return {"output": f"Error: {e.output}"}
