# createEnclovApp.py

import os
from pathlib import Path

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

def create_backend():
    write_file(Path("backend/app/main.py"), """
from fastapi import FastAPI
from app.routes import llm

app = FastAPI()
app.include_router(llm.router, prefix="/api")
    """)

    write_file(Path("backend/app/routes/llm.py"), """
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/llm")
def get_model_info():
    return {
        "model": settings.model_name,
        "temperature": settings.temperature
    }
    """)

    write_file(Path("backend/app/core/config.py"), """
from pydantic import BaseSettings

class Settings(BaseSettings):
    model_name: str = "gpt-4"
    temperature: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()
    """)

    write_file(Path("backend/requirements.txt"), """
fastapi
uvicorn
pydantic
python-dotenv
    """)

    write_file(Path("backend/Dockerfile"), """
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    """)

def create_frontend():
    os.system("npm create vite@latest frontend -- --template react-ts")
    os.chdir("frontend")
    os.system("npm install")
    os.chdir("..")

def create_docker_compose():
    write_file(Path("docker-compose.yml"), """
version: "3.9"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENV=prod

  frontend:
    build:
      context: ./frontend
    ports:
      - "5173:5173"
    command: ["npm", "run", "dev"]

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
      - frontend
    """)

def create_nginx():
    write_file(Path("nginx/default.conf"), """
server {
    listen 80;

    location / {
        proxy_pass http://frontend:5173;
    }

    location /api/ {
        proxy_pass http://backend:8000;
    }
}
    """)

def create_github_workflow():
    write_file(Path(".github/workflows/pr-check.yml"), """
name: PR Check

on:
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Lint Frontend
        run: |
          cd frontend
          npm install
          npm run lint

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Backend Lint
        run: |
          cd backend
          pip install flake8 -r requirements.txt
          flake8 app
    """)

def create_env():
    write_file(Path(".env"), """
MODEL_NAME=gpt-4
TEMPERATURE=0.7
    """)

def create_readme():
    write_file(Path("README.md"), """
# enclov-AI

Production-ready AI app with FastAPI backend, Vite + React frontend, and Docker/CI integration.
    """)

def main():
    create_backend()
    create_frontend()
    create_docker_compose()
    create_nginx()
    create_github_workflow()
    create_env()
    create_readme()
    print("✅ enclov-AI scaffold created!")

if __name__ == "__main__":
    main()
