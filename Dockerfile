FROM python:3.11.9-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD python app/main.py