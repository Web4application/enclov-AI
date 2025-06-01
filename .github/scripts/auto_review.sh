#!/bin/bash
PR_NUMBER=$1
gh pr checkout "$PR_NUMBER"

DIFF=$(gh pr diff "$PR_NUMBER")
REVIEW=$(python3 ai/review_diff.py --diff <(echo "$DIFF"))

gh pr comment "$PR_NUMBER" --body "$REVIEW"
