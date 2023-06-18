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
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]