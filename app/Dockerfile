FROM python:3.10-alpine

RUN apk update
RUN apk add --no-cache gcc musl-dev \
    libpq-dev build-base postgresql-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install "fastapi[all]"
RUN pip install pytest install psycopg2==2.9.5 psycopg2-binary==2.9.5 alembic==1.10.4

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]