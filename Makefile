DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml

up:
	@echo "Bringing up Docker containers..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

build:
	@echo "Building and bringing up Docker containers with --build..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build

down:
	@echo "Stopping and removing containers and volumes..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v

clean:
	@echo "Removing unused containers, volumes, and images..."
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
	docker volume prune -f
	docker network prune -f

logs:
	@echo "Displaying container logs..."
	$(DOCKER_COMPOSE) logs -f

status:
	@echo "Checking container status..."
	$(DOCKER_COMPOSE) ps

test:
	@echo "Running tests with pytest..."
	docker-compose run --rm app pytest

.PHONY: up build down clean logs status test