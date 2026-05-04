FROM python:3.14-slim

RUN rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY pyproject.toml poetry.lock .env ./
COPY src/ ./src/
COPY tests/ ./tests/

RUN pip install poetry &&\
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

ENV PYTHONPATH="/app"

CMD ["python3", "src/api_atlaxoasis_2026/main.py"]