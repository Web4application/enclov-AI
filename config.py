import os

MODEL_CONFIG = {
    "default_model": os.getenv("AI_MODEL", "openai/gpt-4.1"),
    "models": {
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model_name": "openai/gpt-4.1"
        },
        "github": {
            "base_url": "https://models.github.ai/inference",
            "model_name": "openai/gpt-4.1"
        },
        # Add more models here as needed
    }
}

def get_model_config(provider_key="github"):
    provider = MODEL_CONFIG["models"].get(provider_key, MODEL_CONFIG["models"]["openai"])
    return provider["base_url"], provider["model_name"]
