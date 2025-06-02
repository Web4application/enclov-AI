.PHONY: patch unpatch commit-patch

patch:
	./apply_patches.sh

unpatch:
	./revert_patches.sh

commit-patch:
	git add .github/workflows/
	git commit -m "🔧 Applied GitHub workflow permission patches"

push:
	git push origin main

generate-patches:
	./generate_patches.sh
