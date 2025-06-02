#!/bin/bash

set -e  # Exit immediately if a command fails

echo "📦 Creating and applying patch..."

# Step 1: Write the patch file
cat << 'EOF' > fix-gen-man-permissions.patch
diff --git a/.github/workflows/gen-man.yml b/.github/workflows/gen-man.yml
--- a/.github/workflows/gen-man.yml
+++ b/.github/workflows/gen-man.yml
@@ -2,2 +2,5 @@
 
+permissions:
+  contents: read
+
 on:
EOF

# Step 2: Apply the patch
git apply fix-gen-man-permissions.patch
echo "✅ Patch applied successfully."

# Step 3: Stage the changes
git add .github/workflows/gen-man.yml

# Step 4: Commit
git commit -m "🔐 Add permissions: contents read to gen-man GitHub workflow"

# Step 5: Optional push (uncomment if you're ready to push)
# git push origin main

echo "🎉 All done!"
