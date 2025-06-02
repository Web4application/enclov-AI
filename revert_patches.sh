#!/bin/bash

set -e

echo "🧹 Reverting applied patches..."

for patch in patches/*.patch; do
  echo "↩️ Reverting $patch..."
  git apply -R "$patch"
done

echo "✅ All patches reverted."
