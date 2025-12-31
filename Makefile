.PHONY: dev prod down

dev:
	docker compose -f compose.dev.yml up --build

prod:
	docker compose -f compose.prod.yml up --build

down:
	docker compose down
