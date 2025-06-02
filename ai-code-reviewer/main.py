import os
import openai
import requests
from github import Github

openai.api_key = os.getenv("OPENAI_API_KEY")
gh = Github(os.getenv("GITHUB_TOKEN"))

def get_pr_info():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("GITHUB_REF").split('/')[-1])
    return gh.get_repo(repo).get_pull(pr_number)

def get_changed_code(pr):
    diff_url = pr.diff_url
    r = requests.get(diff_url, headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"})
    r.raise_for_status()
    return r.text

def review_code(code_diff):
    prompt = f"""
You are a senior code reviewer. Review this GitHub pull request diff.
Give concise, constructive feedback on improvements, bugs, or best practices.

Diff:
{code_diff[:3000]}  # OpenAI token limit safety

Review:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def post_review(pr, review):
    pr.create_issue_comment(f"🧠 **AI Code Review:**\n\n{review}")

def main():
    pr = get_pr_info()
    code_diff = get_changed_code(pr)
    review = review_code(code_diff)
    post_review(pr, review)

if __name__ == "__main__":
    main()
