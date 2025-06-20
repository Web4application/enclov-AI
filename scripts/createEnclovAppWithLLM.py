from pathlib import Path

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# Combine LangChain + WebLLM into a single `createEnclovAppWithLLM.py` scaffold file
scaffold_script_path = Path("createEnclovAppWithLLM.py")

scaffold_script_code = """
import os
from pathlib import Path

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\\n")

def create_backend():
    write_file(Path("backend/app/main.py"), '''
from fastapi import FastAPI
from app.routes import llm, langagent

app = FastAPI()
app.include_router(llm.router, prefix="/api")
app.include_router(langagent.router, prefix="/api")
    ''')

    write_file(Path("backend/app/routes/llm.py"), '''
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/llm")
def get_model_info():
    return {
        "model": settings.model_name,
        "temperature": settings.temperature
    }
    ''')

    write_file(Path("backend/app/routes/langagent.py"), '''
from fastapi import APIRouter
from app.services.langchain_agent import run_agent

router = APIRouter()

@router.get("/agent")
def ask_agent(q: str):
    return {"response": run_agent(q)}
    ''')

    write_file(Path("backend/app/core/config.py"), '''
from pydantic import BaseSettings

class Settings(BaseSettings):
    model_name: str = "gpt-4"
    temperature: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()
    ''')

    write_file(Path("backend/app/services/langchain_agent.py"), '''
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun

llm = ChatOpenAI(temperature=0, model="gpt-4")
search = DuckDuckGoSearchRun()
tools = [
    Tool(name="Search", func=search.run, description="Search the web for info"),
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def run_agent(prompt: str):
    return agent.run(prompt)
    ''')

    write_file(Path("backend/requirements.txt"), '''
fastapi
uvicorn
pydantic
python-dotenv
openai
langchain
tiktoken
duckduckgo-search
    ''')

    write_file(Path("backend/Dockerfile"), '''
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ''')

def create_frontend():
    os.system("npm create vite@latest frontend -- --template react-ts")
    os.chdir("frontend")
    os.system("npm install @mlc-ai/web-llm")
    os.chdir("..")
    write_file(Path("frontend/src/hooks/useWebLLM.ts"), '''
import { useEffect, useState } from "react";
import { ChatModule } from "@mlc-ai/web-llm";

export const useWebLLM = () => {
  const [chat, setChat] = useState<ChatModule | null>(null);
  const [reply, setReply] = useState<string>("");

  useEffect(() => {
    const loadModel = async () => {
      const chatModule = new ChatModule();
      await chatModule.reload("Llama-3-8B-Instruct-q4f32_1");
      setChat(chatModule);
    };
    loadModel();
  }, []);

  const ask = async (prompt: string) => {
    if (chat) {
      await chat.resetChat();
      await chat.generate(prompt, (chunk: string) => {
        setReply(prev => prev + chunk);
      });
    }
  };

  return { reply, ask };
};
    ''')

def create_docker_compose():
    write_file(Path("docker-compose.yml"), '''
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
    ''')

def create_nginx():
    write_file(Path("nginx/default.conf"), '''
server {
    listen 80;

    location / {
        proxy_pass http://frontend:5173;
    }

    location /api/ {
        proxy_pass http://backend:8000;
    }
}
    ''')

def create_github_workflow():
    write_file(Path(".github/workflows/pr-check.yml"), '''
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
    ''')

def create_env():
    write_file(Path(".env"), '''
MODEL_NAME=gpt-4
TEMPERATURE=0.7
OPENAI_API_KEY=sk-yourkey
    ''')

def create_readme():
    write_file(Path("README.md"), '''
# enclov-AI

Modular AI framework with:
- FastAPI + LangChain backend
- React + WebLLM frontend
- Docker, GitHub Actions, NGINX
    ''')

def main():
    create_backend()
    create_frontend()
    create_docker_compose()
    create_nginx()
    create_github_workflow()
    create_env()
    create_readme()
    print("✅ enclov-AI + WebLLM + LangChain scaffold created!")

if __name__ == "__main__":
    main()
"""

write_file(scaffold_script_path, scaffold_script_code)

scaffold_script_path.name

