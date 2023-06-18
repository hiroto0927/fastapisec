FROM mcr.microsoft.com/devcontainers/python:3.10-bullseye

RUN apt update

RUN apt-get install -y --no-install-recommends \
    gcc \
    musl-dev \
    libpq-dev \
    build-essential \
    postgresql-server-dev-all \
    python3-dev \
    libffi-dev \
    openssl \
    docker \
    docker-compose \
    && rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /workspaces
