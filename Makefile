.PHONY: patch unpatch commit-patch push generate-patches

patch:
	@echo "🩹 Applying patches..."
	@chmod +x scripts/apply_patches.sh
	@scripts/apply_patches.sh || (echo "❌ Patch application failed." && exit 1)
	@echo "✅ Patches applied."

unpatch:
	@echo "↩️ Reverting patches..."
	@chmod +x scripts/revert_patches.sh
	@scripts/revert_patches.sh || (echo "❌ Revert failed." && exit 1)
	@echo "✅ Patches reverted."

commit-patch:
	@git add .github/workflows/
	@git diff --cached --quiet || git commit -m "🔧 Applied GitHub workflow permission patches"
	@echo "✅ Patch commit ready."

push:
	@git push origin HEAD
	@echo "🚀 Changes pushed."

generate-patches:
	@echo "📦 Generating patch files..."
	@chmod +x scripts/generate_patches.sh
	@scripts/generate_patches.sh
	@echo "✅ Patch files generated."


APP_NAME=enclov-AI

deploy:
	./deploy.sh

watch:
	./deploy.sh --watch

logs:
	docker-compose -f $(APP_NAME)/docker-compose.yml logs -f

stop:
	docker-compose -f $(APP_NAME)/docker-compose.yml down
