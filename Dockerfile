FROM python:3.11-slim-bullseye

RUN groupadd -g 999 keithfembot && \
    useradd -u 999 -g 999 -m -d /keithfembot keithfembot
RUN mkdir /keithfembot/keithfembot

COPY ./src /keithfembot/keithfembot/src
COPY ./poetry.lock /keithfembot/keithfembot/poetry.lock
COPY ./pyproject.toml /keithfembot/keithfembot/pyproject.toml

RUN python -m venv /keithfembot/venv && \
    /keithfembot/venv/bin/pip install -U pip setuptools && \
    /keithfembot/venv/bin/pip install poetry

ENV PATH="/keithfembot/venv/bin:$PATH"

WORKDIR /keithfembot/keithfembot
RUN poetry config virtualenvs.create false
RUN poetry install
USER keithfembot
CMD python /keithfembot/keithfembot/src/keithfembot.py
