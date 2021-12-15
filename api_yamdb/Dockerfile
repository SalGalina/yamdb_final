FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir

RUN chmod -R 655 static/

CMD gunicorn api_yamdb.wsgi:application --bind 0:8000

LABEL org.opencontainers.image.source=https://github.com/salgalina/api_yamdb
