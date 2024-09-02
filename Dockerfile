FROM python:3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN python -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl libpq-dev libpango-1.0-0 libpangoft2-1.0-0 libmagic1 ffmpeg poppler-utils \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY --from=builder /venv/ /venv/
COPY . /app/

EXPOSE 8080
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
