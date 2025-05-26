# Start from official Python slim image for a lean base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency files first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run your FastAPI app (adjust main:app if different)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
