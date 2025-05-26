# enclov/api/app.py

from fastapi import FastAPI
from enclov.config.model_config import DEFAULT_MODEL_NAME, DEVICE

app = FastAPI(title="enclov-AI API")

@app.get("/status")
async def status():
    return {
        "status": "ok",
        "default_model": DEFAULT_MODEL_NAME,
        "device": DEVICE,
    }

@app.get("/models")
async def models():
    # Return list of supported models
    from enclov.config.model_config import MODELS
    return {"models": [m.repo for m in MODELS]}
