# enclov-AI 🧠🤖

**AI-Powered GitHub Pull Request Reviewer**  
_Automate code reviews with GPT-powered intelligence. FastAPI + Celery + Redis. Dockerized & DevOps-ready._

---

## ✨ Overview

`enclov-AI` is your AI sidekick for PR reviews. It listens to GitHub webhook events, analyzes code diffs using OpenAI models, and posts smart, context-aware comments right into your pull requests.

Whether you're tired of nitpicks, want consistent reviews, or just love dev automation — `enclov-AI` ships your code with confidence.

---

## 🚀 Features

- ✅ **GPT-powered code review suggestions**
- 🔄 **GitHub webhook integration**
- ⏱️ **Async processing with Celery & Redis**
- 🐳 **Full Docker support for dev/prod**
- 🛡️ **Scalable FastAPI backend**
- 🧪 Unit-tested core logic (soon™)

---

## 🛠️ Architecture

```

GitHub Webhook → FastAPI Web Server → Celery Task Queue → OpenAI API
↓
Redis (Broker)

````

---

## 📦 Tech Stack

| Layer         | Tech                    |
|---------------|-------------------------|
| Backend       | FastAPI                 |
| AI Review     | OpenAI GPT (via API)    |
| Async Queue   | Celery + Redis          |
| Deployment    | Docker / Vercel         |
| Frontend      | Static HTML (Dark UI)   |

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/Web4application/enclov-AI.git
cd enclov-AI
````

### 🐳 Docker (Full stack)

```bash
docker-compose up --build
```

By default, this starts:

* `api`: FastAPI backend on `http://localhost:8000`
* `worker`: Celery task processor
* `redis`: Message broker

---

## 🔐 Environment Setup

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your_openai_key_here
GITHUB_APP_SECRET=your_github_webhook_secret
```

You can generate GitHub secrets under your App configuration.

---

## 🧪 Webhook Testing

* Use [smee.io](https://smee.io/) or ngrok to tunnel `http://localhost:8000/webhook/github`
* Push a PR to your GitHub repo
* Watch the logs for the AI-generated feedback

---

## 📤 Deployment

### ✅ Local Dev

Use Docker Compose (see `docker-compose.yml`):

```bash
docker-compose up
```

### 🌐 Vercel Frontend + Backend

You can deploy the static HTML to [Vercel](https://vercel.com/) and the FastAPI backend separately (Render, Fly.io, Railway).

---

## 🧠 Want to Extend?

* Add support for GitHub Checks API or GitHub Comments
* Integrate Claude/Sonar/CodeQL for hybrid analysis
* Add CI/CD with GitHub Actions to auto-deploy containers

---

## 👤 Author

**Kubu Lee**
[GitHub](https://github.com/Web4application) • `enclov-AI` Maintainer • Builder of AI, Web4, & Insight Engines

---

## 🛡️ License

MIT — Use it, fork it, AI-ify your stack.

````

---

## ⚙️ `deploy.sh` — Dev/Prod Deployment Script

```bash
#!/bin/bash
set -e

APP_NAME="enclov-AI"
REPO_URL="https://github.com/Web4application/enclov-AI.git"
FRONTEND_PATH="./index.html"
BACKEND_PATH="./app"
VERCEL_PROJECT_NAME="enclov-ai-frontend"

echo "🚀 Deploying $APP_NAME..."

# Step 1: Pull latest
if [ ! -d "$APP_NAME" ]; then
  git clone $REPO_URL
else
  echo "🔄 Repo already exists. Pulling latest..."
  cd $APP_NAME && git pull && cd ..
fi

cd $APP_NAME

# Step 2: Check Docker Compose
echo "🐳 Starting Docker Compose stack..."
docker-compose up -d --build

# Step 3: Vercel Frontend Deploy (if installed)
if command -v vercel &> /dev/null; then
  echo "🌐 Deploying static frontend to Vercel..."
  cd frontend || mkdir frontend && cp $FRONTEND_PATH frontend/index.html && cd frontend
  vercel --prod --confirm --name "$VERCEL_PROJECT_NAME"
  cd ..
else
  echo "⚠️ Vercel CLI not found. Skipping frontend deploy."
  echo "Install via: npm i -g vercel"
fi

echo "✅ Deployment complete."
````

> 💡 Optional: Add GitHub Actions for CI/CD. Want me to scaffold it?
