import os
import openai
import requests
from github import Github, PullRequest

def get_github_client(token: str) -> Github:
    return Github(token)

def get_pr(pr_number: int, repo_name: str, gh: Github) -> PullRequest.PullRequest:
    return gh.get_repo(repo_name).get_pull(pr_number)

def fetch_pr_files(pr: PullRequest.PullRequest):
    return pr.get_files()

def fetch_patch_from_file(file) -> str:
    return file.patch  # GitHub provides diff patch per file

def split_patch_into_hunks(patch: str) -> list:
    """Naively split a patch into hunks by @@ marker"""
    return patch.split("\n@@")[1:] if patch else []

def review_patch_hunk(hunk: str, filename: str) -> str:
    prompt = f"""
You are a senior software engineer. Review the following code patch (diff hunk) in file `{filename}`.
Identify any bugs, bad practices, or improvements. Be specific and constructive.

Patch:
{hunk}

Review:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=400,
    )
    return response.choices[0].message.content.strip()

def add_inline_review_comments(pr: PullRequest.PullRequest, gh: Github, openai_key: str):
    openai.api_key = openai_key
    repo = pr.base.repo
    files = fetch_pr_files(pr)
    review_comments = []

    for file in files:
        if not file.filename.endswith(('.py', '.js', '.ts', '.go', '.java')):
            continue

        patch = fetch_patch_from_file(file)
        hunks = split_patch_into_hunks(patch)
        
        for hunk in hunks:
            try:
                review = review_patch_hunk(hunk, file.filename)
                if not review.strip():
                    continue

                # GitHub API needs exact position, fallback to 1st line of hunk
                position = 1  
                comment = {
                    "path": file.filename,
                    "body": f"🧠 **AI Review Suggestion:**\n\n{review}",
                    "position": position
                }
                review_comments.append(comment)

            except Exception as e:
                pr.create_issue_comment(f"⚠️ Failed to review a hunk in `{file.filename}`: {e}")

    if review_comments:
        repo._requester.requestJson(
            "POST",
            f"{repo.url}/pulls/{pr.number}/reviews",
            input={
                "body": "🤖 AI Code Review: Inline suggestions for improvement",
                "event": "COMMENT",
                "comments": review_comments
            }
        )
