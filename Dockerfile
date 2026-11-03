# Multi-stage Dockerfile for Car Price Prediction Inference API
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-api.txt .
RUN pip install --no-cache-dir --user -r requirements-api.txt

# Final Production Image
FROM python:3.11-slim

WORKDIR /app

# Non-root user for security best practices
RUN useradd -m -u 1000 appuser

# Copy installed wheels and dependencies
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code and deployment artifacts
COPY api/ /app/api/
COPY deployment/ /app/deployment/
COPY models/ /app/models/
COPY config.yaml /app/config.yaml

# Create directory for runtime inference logging
RUN mkdir -p /app/logs/inference && chown -R appuser:appuser /app

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
