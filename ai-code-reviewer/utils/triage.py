import openai

LABEL_MAP = {
    "bug": ["fix", "broken", "issue", "error", "fails", "unexpected"],
    "refactor": ["refactor", "cleanup", "structure", "reorganize"],
    "docs": ["readme", "documentation", "comment", "docs"],
    "feature": ["add", "introduce", "implement", "new"],
    "security": ["vulnerability", "exploit", "xss", "sql injection", "leak"]
}

REVIEWER_MAP = {
    "frontend": ["src/components", "web/", "ui/"],
    "backend": ["api/", "server/", "routes/", "models/"],
    "security": ["auth/", "encryption/", "security/"],
    "docs": ["docs/", "README.md"],
}


def analyze_pr_with_openai(title: str, body: str, files: list, model="gpt-4o-mini"):
    prompt = f"""
You are an AI code triage assistant. Given the following GitHub PR title, description, and modified filenames,
summarize the purpose of this PR and suggest appropriate labels from: {', '.join(LABEL_MAP.keys())}.

PR Title:
{title}

PR Description:
{body}

Changed Files:
{files}

Your Response (JSON):
{{"summary": "...", "labels": ["label1", "label2", ...]}}
"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )

    content = response.choices[0].message.content.strip()
    return content


def extract_labels_from_ai(json_str: str) -> tuple:
    import json
    try:
        parsed = json.loads(json_str)
        return parsed.get("summary", ""), parsed.get("labels", [])
    except Exception:
        return "", []


def match_reviewers_by_paths(file_paths: list) -> list:
    reviewers = set()
    for path in file_paths:
        for category, dirs in REVIEWER_MAP.items():
            if any(path.startswith(d) for d in dirs):
                reviewers.add(category)
    return list(reviewers)
