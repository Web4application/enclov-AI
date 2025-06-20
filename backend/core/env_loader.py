import os
from dotenv import load_dotenv

# Load .env file only in local/dev environment
if os.getenv("ENV", "development") == "development":
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(dotenv_path)

# Unified access point for all sensitive environment variables
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Optional safety checks
missing = [k for k, v in {
    "GITHUB_WEBHOOK_SECRET": GITHUB_WEBHOOK_SECRET,
    "GITHUB_ACCESS_TOKEN": GITHUB_ACCESS_TOKEN,
    "OPENAI_API_KEY": OPENAI_API_KEY,
}.items() if not v]

if missing:
    raise EnvironmentError(f"Missing env variables: {', '.join(missing)}")
