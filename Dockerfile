FROM python:3.11-slim
LABEL maintainer="borgarc"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

EXPOSE 8000

ARG DEV=true

RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y postgresql-client build-essential libpq-dev && \
    pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser --disabled-password django-user

ENV PATH="/py/bin:$PATH"

COPY . /app
WORKDIR /app

RUN mkdir -p /tmp && chmod 1777 /tmp
USER django-user
