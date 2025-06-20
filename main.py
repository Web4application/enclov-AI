import os
import json
from github import Github
from utils import github_inline, triage
import openai

def main():
    github_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("GITHUB_REF").split("/")[-2])

    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    openai.api_key = openai_key

    # Inline AI Review
    github_inline.add_inline_review_comments(pr, gh, openai_key)

    # AI PR Triage (Summary + Labels + Reviewers)
    files_changed = [f.filename for f in pr.get_files()]
    ai_response = triage.analyze_pr_with_openai(pr.title, pr.body or "", files_changed)
    summary, labels = triage.extract_labels_from_ai(ai_response)

    if summary:
        pr.create_issue_comment(f"🧠 **AI Summary:**\n\n{summary}")
    
    if labels:
        pr.add_to_labels(*labels)

    reviewers = triage.match_reviewers_by_paths(files_changed)
    if reviewers:
        pr.create_review_request(reviewers=reviewers)

if __name__ == "__main__":
    main()
