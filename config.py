import os

class Settings:
    OPENAI_API_KEY = os.getenv("Sk-gG1uZhj50x1lYFKrrB5kT3BlbkFJXP3R63ExWT9lkcHI0pRq")
    GOOGLE_API_KEY = os.getenv("AlzaSyCHjfdo3w160Dd5yTVJD409pWmigOJEg")
    PROVIDER = os.getenv("PROVIDER", "enclovai")  # "openai", "google", or "enclovai"

settings = Settings()


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
