FROM python:3.8.3-alpine3.11
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

ENV no_proxy="127.0.0.1, localhost"

RUN mkdir /docker_build
COPY requirements.txt /docker_build/requirements.txt
WORKDIR /docker_build

RUN apk update
RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
	bash
RUN pip install -r requirements.txt

COPY ./ /app
WORKDIR /app

EXPOSE 8000

CMD gunicorn -b :8000 bp.wsgi