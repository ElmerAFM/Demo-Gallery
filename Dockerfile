FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Copy dependency files first (cache-friendly)
COPY pyproject.toml uv.lock ./

# Install build & runtime dependencies temporarily
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      gcc \
      default-libmysqlclient-dev \
      pkg-config \
      python3-dev \
 && uv sync --frozen --python /usr/local/bin/python3 \
 && apt-get purge -y gcc pkg-config python3-dev \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Ensure uploads folder exists
RUN mkdir -p static/uploads

EXPOSE 5000

ENV FLASK_APP=app.py \
    FLASK_ENV=production

CMD ["uv", "run", "--no-sync", "flask", "run", "--host=0.0.0.0", "--port=5000"]
