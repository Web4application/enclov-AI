import random

def analyze_pr(repo_url: str, pr_number: int):
    # Real logic would clone repo, checkout PR diff, run LLM, etc.
    mock_comments = [
        f"✅ Efficient use of data structures in PR #{pr_number}.",
        "🧹 Consider removing unused imports.",
        "🔒 Security tip: mask sensitive keys in logs.",
        "📦 Use semantic versioning in your package updates.",
        "🧠 Consider adding docstrings to helper functions."
    ]
    return random.sample(mock_comments, k=3)
