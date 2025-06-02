# Start from official Python slim base image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies first for speed
RUN apt-get update && apt-get install -y build-essential gcc libffi-dev curl

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies into a dedicated folder
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Final stage: minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy app code
COPY . .

# Use virtualenv's python and pip
ENV PATH="/opt/venv/bin:$PATH"

# Drop root privileges by creating a non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Run uvicorn with optimized flags
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--loop", "uvloop", "--http", "h11"]
