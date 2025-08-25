.DEFAULT_GOAL := help

start: ## Start services using docker-compose in detached mode
	docker-compose up

stop: ## Stop all services
	docker-compose down

logs: ## View logs
	docker-compose logs -f

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create: ## Create a new migration
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply: ## Apply migrations
	alembic upgrade head

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
