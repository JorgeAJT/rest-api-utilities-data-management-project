FROM python:3.12.0 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN python -m venv .venv
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12.0-slim

WORKDIR /app

COPY --from=builder /app/.venv .venv/
COPY src/ src/
COPY main.py .

ENV DB_NAME=users-db
ENV DB_USER=root
ENV DB_HOST=users-db-container
ENV DB_PORT=5432
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8080

EXPOSE 8080
CMD [".venv/bin/python", "main.py"]
