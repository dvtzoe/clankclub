.PHONY: dev prod down migrate migrate-prod

dev:
	docker compose -f compose.dev.yml up --build

prod:
	docker compose -f compose.prod.yml up --build

down:
	docker compose down

migrate:
	docker compose -f compose.dev.yml exec backend uv run alembic upgrade head

migrate-prod:
	docker compose -f compose.prod.yml exec backend uv run alembic upgrade head

