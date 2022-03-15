FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD pyproject.toml poetry.lock /code/

RUN pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install
