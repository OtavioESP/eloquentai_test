# RAG Chat Application Makefile

.PHONY: help build up down logs clean restart status

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build all Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - View logs for all services"
	@echo "  logs-api  - View logs for API service"
	@echo "  logs-db   - View logs for database service"
	@echo "  logs-ui   - View logs for frontend service"
	@echo "  restart   - Restart all services"
	@echo "  clean     - Stop services and remove volumes"
	@echo "  status    - Show status of all services"
	@echo "  shell-api - Open shell in API container"
	@echo "  shell-db  - Open shell in database container"

# Build all images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Start with build
up-build:
	docker-compose up --build -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# View API logs
logs-api:
	docker-compose logs -f api

# View database logs
logs-db:
	docker-compose logs -f postgres

# View frontend logs
logs-ui:
	docker-compose logs -f frontend

# Restart all services
restart:
	docker-compose restart

# Clean up (stop and remove volumes)
clean:
	docker-compose down -v
	docker system prune -f

# Show status
status:
	docker-compose ps

# Open shell in API container
shell-api:
	docker-compose exec api /bin/bash

# Open shell in database container
shell-db:
	docker-compose exec postgres psql -U postgres -d rag_chat

# Run migrations manually
migrate:
	docker-compose exec api python migrations/run_migrations.py up

# Test database connection
test-db:
	docker-compose exec api python database.py
