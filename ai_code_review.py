import os
import requests
from github import Github
from project_pilot_ai.github_models import ModelClient
from project_pilot_ai.config import get_model_config

# Environment
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))
ai_model = os.getenv("AI_MODEL", "github")

# AI client setup
base_url, model_name = get_model_config(ai_model)
client = ModelClient(base_url=base_url, model=model_name, token=token)

# GitHub API setup
g = Github(token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)
files = pr.get_files()

# Construct file change summary
changed_files = "\n".join(f.filename for f in files)
diff_summary = []
for f in files:
    diff = f.patch if hasattr(f, "patch") else "[No diff available]"
    diff_summary.append(f"\n--- {f.filename} ---\n{diff[:1000]}")  # Limit long diffs
diff_text = "\n".join(diff_summary)

# Prompt for AI review
system_msg = {
    "role": "system",
    "content": (
        "You are a senior software engineer reviewing a GitHub Pull Request. "
        "Focus on maintainability, clarity, and security. Provide clear suggestions and praise good code."
    ),
}
user_msg = {
    "role": "user",
    "content": (
        f"Here are the changed files:\n{changed_files}\n\n"
        f"Here is the diff summary:\n{diff_text}\n\n"
        f"Please review the pull request and offer constructive feedback."
    ),
}

print("[🤖] Asking AI for review...")
response = client.ask([system_msg, user_msg])
print("[✅] AI Review Response:\n", response)

# Post as PR comment
comment_body = f"""
### 🤖 AI Code Review Summary

**Files Changed:**
