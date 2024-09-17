DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml

up:
	@echo "Subindo os containers do Docker..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

build:
	@echo "Construindo e subindo os containers do Docker com --build..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build

down:
	@echo "Parando e removendo containers e volumes..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v

clean:
	@echo "Removendo containers, volumes e imagens não utilizados..."
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
	docker volume prune -f
	docker network prune -f

logs:
	@echo "Exibindo logs dos containers..."
	$(DOCKER_COMPOSE) logs -f

status:
	@echo "Verificando o status dos containers..."
	$(DOCKER_COMPOSE) ps

test:
	@echo "Rodando testes com pytest..."
	docker-compose run --rm app pytest

.PHONY: up build down clean logs status test
