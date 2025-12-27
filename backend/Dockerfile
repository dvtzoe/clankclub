FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./src /app/src
COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock
COPY ./config.json /app/config.json

ENV UV_NO_DEV=1
ENV CONFIG_PATH=/app/config.json

WORKDIR /app

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
