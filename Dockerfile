# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install uv
COPY pyproject.toml uv.lock* ./
RUN uv pip install -r pyproject.toml

# Install unlisted dependencies detected via AST source scanning
RUN pip install --no-cache-dir core langchain_chroma langchain_core langchain_huggingface langchain_mistralai langchain_text_splitters rich utils

# ==========================================
# Stage 2: Minimal Production Runner
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Install runtime system packages (e.g. ffmpeg, libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Security: Create and use non-root application user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Copy virtualenv from builder stage
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Copy application source code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD ["python", "main.py"]