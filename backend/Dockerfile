FROM python:3.12-slim

WORKDIR /app

# Install curl (used for health checks later)
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (better Docker cache)
COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]