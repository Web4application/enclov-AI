FROM python:3.11-slim

WORKDIR /app

COPY api /app/api
COPY scripts /app/scripts
COPY model_config.yaml /app/model_config.yaml
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
