FROM python:3.13-slim

RUN pip install --upgrade uv
COPY pyproject.toml uv.lock ./
RUN uv sync
RUN apt-get update -y --fix-missing && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY ./app ./app
COPY startup.sh .
COPY alembic.ini .
COPY ./migrations ./migrations
ENV PYTHONPATH=/

CMD ["/bin/sh", "startup.sh"]