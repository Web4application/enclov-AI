import os
import openai
import requests
import difflib
from github import Github, PullRequest

# === Core Setup ===

def init_openai(api_key: str):
    openai.api_key = api_key


def get_github_client(token: str) -> Github:
    return Github(token)


def get_pr_number() -> int:
    ref = os.getenv("GITHUB_REF")
    if not ref or "pull" not in ref:
        raise RuntimeError("GITHUB_REF does not indicate a pull request")
    return int(ref.split("/")[-1])


def get_repo_full_name() -> str:
    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo:
        raise RuntimeError("GITHUB_REPOSITORY is not set")
    return repo


def get_pull_request(gh: Github) -> PullRequest.PullRequest:
    return gh.get_repo(get_repo_full_name()).get_pull(get_pr_number())


# === PR Diff Utilities ===

def fetch_pr_diff(pr: PullRequest.PullRequest) -> str:
    diff_url = pr.diff_url
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(diff_url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_diff_by_file(diff_text: str) -> dict:
    """Parse unified diff into {filename: diff_content}"""
    files = {}
    current_file = None
    current_diff = []

    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            if current_file and current_diff:
                files[current_file] = "\n".join(current_diff)
            current_file = line.split(" b/")[-1]
            current_diff = [line]
        elif current_file:
            current_diff.append(line)

    if current_file and current_diff:
        files[current_file] = "\n".join(current_diff)

    return files


def filter_files_by_extension(files: dict, exts=(".py", ".js", ".ts", ".go", ".java")) -> dict:
    return {fname: diff for fname, diff in files.items() if fname.endswith(exts)}


def split_into_chunks(text: str, max_chars: int = 3000) -> list:
    """Split large diffs into smaller chunks for OpenAI API"""
    lines = text.splitlines()
    chunks = []
    chunk = []

    current_len = 0
    for line in lines:
        line_len = len(line) + 1
        if current_len + line_len > max_chars:
            chunks.append("\n".join(chunk))
            chunk = []
            current_len = 0
        chunk.append(line)
        current_len += line_len

    if chunk:
        chunks.append("\n".join(chunk))

    return chunks


# === OpenAI Review ===

def review_diff_with_openai(diff: str, model: str = "gpt-4o-mini") -> str:
    prompt = f"""
You are a senior code reviewer. Review this GitHub PR diff. Give useful, concise feedback on code quality, bugs, design, and best practices.

Diff:
{diff}

Review:
""".strip()

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# === PR Commenting ===

def post_review_comment(pr: PullRequest.PullRequest, review: str):
    pr.create_issue_comment(f"🧠 **AI Code Review**\n\n{review}")


def post_chunked_reviews(pr: PullRequest.PullRequest, diff_text: str):
    files = parse_diff_by_file(diff_text)
    files = filter_files_by_extension(files)

    for fname, file_diff in files.items():
        chunks = split_into_chunks(file_diff)
        for i, chunk in enumerate(chunks):
            try:
                review = review_diff_with_openai(chunk)
                heading = f"🧠 Review for `{fname}` (chunk {i+1})"
                pr.create_issue_comment(f"{heading}:\n\n{review}")
            except Exception as e:
                pr.create_issue_comment(f"⚠️ Error reviewing `{fname}` chunk {i+1}: {e}")
