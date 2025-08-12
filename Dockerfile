FROM python:3.13 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

RUN curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/download/0.6.12/uv-installer.sh | sh

# Install Python dependencies
COPY pyproject.toml /app/
RUN /root/.local/bin/uv sync

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl libpq-dev libmagic1 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY --from=builder /app/.venv/ /app/.venv/
COPY --from=builder /app/uv.lock /app/
COPY neuesvomtage/ /app/
COPY entrypoint.sh /app/

EXPOSE 8080
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
