# models.py or database.py

def save_review_comments(repo_url: str, pr_number: int, comments: list):
    print(f"Saving review for {repo_url} PR #{pr_number}")
    for comment in comments:
        print(f"- {comment}")
