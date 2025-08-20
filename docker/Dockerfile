FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    USE_DOCKER=1 \
    LANG=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    LC_TIME=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gcc \
    gettext \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM base AS development
COPY . .
RUN uv sync --frozen
CMD ["uv", "run", "python", "app/main.py"]

FROM base AS production
COPY ./app ./app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "python", "app/main.py"]