FROM python:3.10-alpine

RUN apk update
RUN apk add --no-cache gcc musl-dev \
    libpq-dev build-base postgresql-dev
RUN apk add --no-cache python3-dev libffi-dev openssl-dev cargo pkgconfig

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]