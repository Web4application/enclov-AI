# AI-Powered PR Code Reviewer

This repository hosts an AI-powered GitHub pull request code review system that analyzes diffs and posts review comments automatically.

## Features

- Analyzes PR diffs using AI to identify bugs, security issues, and style problems.
- Posts AI-generated review comments directly on the PR.
- Runs automatically on PR open, update, or reopen events.
- Easy to extend with new languages, prompts, and integrations.

## Setup

1. **Create a GitHub repository** and push this code.

2. **Add the GitHub Actions workflow** in `.github/workflows/ai_pr_review.yml`.

3. **Ensure your repo has a GitHub token** set as a secret (usually `GITHUB_TOKEN` is provided automatically).

4. **Configure environment variables** as needed if running locally (see `.env.example`).

5. **Push a PR** to trigger the workflow and see AI comments on your PR.

## Development

- The main logic is in `ai_code_review.py`.
- Modify prompts or add parsing logic to improve AI feedback precision.
- Add support for inline comments by mapping AI feedback to diff positions.

## Contribution

Contributions, issues, and feature requests are welcome. Please open an issue or pull request.

---

**Keep your code clean. Let AI handle the hard part.**

