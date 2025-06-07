# utils/github_client.py

import requests

def fetch_pull_request_diff(repo_url: str, pr_number: int) -> str:
    owner_repo = repo_url.replace("https://github.com/", "")
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "Authorization": f"Bearer YOUR_GITHUB_TOKEN"
    }
    url = f"https://api.github.com/repos/{owner_repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else ""
