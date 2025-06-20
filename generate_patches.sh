#!/bin/bash

set -e

PATCH_DIR="patches"
WORKFLOW_DIR=".github/workflows"

mkdir -p "$PATCH_DIR"

echo "🔍 Scanning for workflow changes in $WORKFLOW_DIR..."

for file in $(git diff --name-only "$WORKFLOW_DIR"); do
  if [[ -f "$file" ]]; then
    base=$(basename "$file")
    patch_name="$PATCH_DIR/fix-${base%.yml}.patch"
    echo "🧬 Creating patch: $patch_name"
    git diff "$file" > "$patch_name"
  fi
done

echo "✅ Patch files generated in $PATCH_DIR/"

# Inside the loop:
if git diff "$file" | grep -q .; then
  git diff "$file" > "$patch_name"
else
  echo "⚠️  No diff for $file – skipping"
fi
