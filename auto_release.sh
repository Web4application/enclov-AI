#!/bin/bash
TAG=$1
COMMITS=$(git log --oneline HEAD~10..HEAD)
RELEASE_NOTES=$(python3 ai/generate_patchnotes.py --commits "$COMMITS")

gh release create "$TAG" --title "Release $TAG" --notes "$RELEASE_NOTES"
