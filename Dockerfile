# Stage 1: Build dependencies
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Install build dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config python3-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a separate directory
RUN uv sync --frozen --no-install-project --python /usr/local/bin/python3

# Stage 2: Final lightweight image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update \
 && apt-get install -y --no-install-recommends default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /root/.cache/uv /root/.cache/uv

# Copy application code
COPY . .

# Create uploads folder
RUN mkdir -p static/uploads

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["uv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
