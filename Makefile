APP_NAME=enclov-AI

DOCKER_COMPOSE_FILE=$(APP_NAME)/docker-compose.yml

DEPLOY_SCRIPT=./deploy.sh

status:
	@scripts/status.sh

cleanup:
	@scripts/cleanup.sh


deploy:
	./deploy.sh

watch:
	./deploy.sh --watch

logs:
	docker-compose -f $(APP_NAME)/docker-compose.yml logs -f

stop:
	docker-compose -f $(APP_NAME)/docker-compose.yml down

.PHONY: deploy watch logs stop restart clean help

deploy:
	@echo "🛠️  Deploying EnclovAI..."
	$(DEPLOY_SCRIPT)

watch:
	@echo "👀 Watching for changes and auto-redeploying..."
	$(DEPLOY_SCRIPT) --watch

logs:
	@echo "📖 Showing Docker logs..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

stop:
	@echo "🛑 Stopping Docker containers..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

restart: stop deploy
	@echo "🔄 Restarted EnclovAI deployment."

clean: stop
	@echo "🧹 Cleaning up Docker containers and images..."
	docker system prune -f

help:
	@echo "Available commands:"
	@echo "  make deploy    - Deploy EnclovAI"
	@echo "  make watch     - Deploy and watch for changes"
	@echo "  make logs      - View Docker logs"
	@echo "  make stop      - Stop Docker containers"
	@echo "  make restart   - Restart deployment"
	@echo "  make clean     - Remove stopped containers and unused images"
	@echo "  make help      - Show this help message"
