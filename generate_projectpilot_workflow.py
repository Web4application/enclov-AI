import os
import argparse

WORKFLOW_YML = """
name: ProjectPilotAI PR Analysis

on:
  pull_request:
    branches:
      - main
      - develop

permissions:
  contents: read
  pull-requests: write

jobs:
  analyze_pr:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Extract AI insights and comment on PR
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          AI_MODEL: {model}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO: ${{ github.repository }}
        run: |
          python -c \"
import os
import requests
from project_pilot_ai.github_models import ModelClient
from project_pilot_ai.config import get_model_config

def fetch_changed_files(repo, pr_number, token):
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files'
    headers = {{'Authorization': f'token {{token}}'}}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()
    return '\\\\n'.join(file['filename'] for file in files)

def post_comment(repo, pr_number, token, comment_body):
    url = f'https://api.github.com/repos/{{repo}}/issues/{{pr_number}}/comments'
    headers = {{
        'Authorization': f'token {{token}}',
        'Accept': 'application/vnd.github.v3+json'
    }}
    response = requests.post(url, headers=headers, json={{'body': comment_body}})
    response.raise_for_status()

repo = os.getenv('REPO')
pr_number = os.getenv('PR_NUMBER')
token = os.getenv('GITHUB_TOKEN')
model_type = os.getenv('AI_MODEL', 'github')

base_url, model_name = get_model_config(model_type)
client = ModelClient(base_url=base_url, model=model_name, token=token)

try:
    file_tree = fetch_changed_files(repo, pr_number, token)
except Exception as e:
    file_tree = 'Could not fetch changed files.'

goals = 'Make the project scalable, maintainable, and secure.'
prompt_repo = f'Analyze the PR changes and project structure:\\\\n{{file_tree}}\\\\nGoals:\\\\n{{goals}}'
repo_response = client.ask([
    {{'role': 'system', 'content': 'You are an expert software architect.'}},
    {{'role': 'user', 'content': prompt_repo}}
])

transcript = 'Task A assigned to John. Refactor login flow by Friday.'
prompt_tasks = f'Extract tasks from meeting transcript: {{transcript}}'
task_response = client.ask([
    {{'role': 'system', 'content': 'You are a helpful assistant.'}},
    {{'role': 'user', 'content': prompt_tasks}}
])

comment_body = f'''
### 🤖 ProjectPilotAI Analysis

**📁 Changed Files:**
