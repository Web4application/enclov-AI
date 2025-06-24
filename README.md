[![Build and Deploy Enclov CLI Docs](https://github.com/Web4application/enclov-AI/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/Web4application/enclov-AI/actions/workflows/deploy-docs.yml)
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



## ⚙️ `deploy.sh` — Dev/Prod Deployment Script

```

#!/bin/bash
set -e

APP_NAME="enclov-AI"
REPO_URL="https://github.com/Web4application/enclov-AI.git"
FRONTEND_PATH="./index.html"
VERCEL_PROJECT_NAME="enclov-ai-frontend"
ENV_FILE=".env"

# Load environment variables (including secrets)
load_env() {
  if [ -f "$ENV_FILE" ]; then
    echo "📦 Loading environment variables from $ENV_FILE"
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
  fi
}

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

send_slack_notification() {
  if [ -n "$SLACK_WEBHOOK_URL" ]; then
    local message="$1"
    curl -s -X POST -H 'Content-type: application/json' \
      --data "{\"channel\": \"$SLACK_CHANNEL\", \"text\": \"$message\"}" \
      "$SLACK_WEBHOOK_URL" > /dev/null 2>&1
  fi
}

send_email_notification() {
  if [ -n "$SENDGRID_API_KEY" ] && [ -n "$EMAIL_TO" ]; then
    local subject="$1"
    local content="$2"

    curl -s --request POST \
      --url https://api.sendgrid.com/v3/mail/send \
      --header "Authorization: Bearer $SENDGRID_API_KEY" \
      --header 'Content-Type: application/json' \
      --data "{
        \"personalizations\": [{ \"to\": [{ \"email\": \"$EMAIL_TO\" }] }],
        \"from\": { \"email\": \"$EMAIL_FROM\" },
        \"subject\": \"$subject\",
        \"content\": [{ \"type\": \"text/plain\", \"value\": \"$content\" }]
      }" > /dev/null
  fi
}

redeploy_on_change() {
  log "🛠️ Watching for file changes in $APP_NAME..."
  inotifywait -r -e modify,create,delete ./frontend ./app |
  while read path _ file; do
    log "🔁 Change detected: $file. Redeploying..."
    ./deploy.sh
  done
}

# Main deploy function
deploy() {
  log "🚀 Deploying $APP_NAME..."

  # Clone or pull latest
  if [ ! -d "$APP_NAME" ]; then
    git clone "$REPO_URL"
  else
    log "🔄 Repo exists. Pulling latest..."
    pushd "$APP_NAME"
    git pull
    LAST_COMMIT=$(git log -1 --pretty=format:"%h - %s by %an")
    popd
  fi

  # Slack notify with commit info
  send_slack_notification ":rocket: *Deploying $APP_NAME started...*\nLast commit: \`$LAST_COMMIT\`"

  cd "$APP_NAME"

  # Docker Compose deploy
  log "🐳 Starting Docker Compose stack..."
  if [ -f "../$ENV_FILE" ]; then
    docker-compose --env-file "../$ENV_FILE" up -d --build
  else
    docker-compose up -d --build
  fi

  # Vercel deploy frontend
  if command -v vercel &> /dev/null; then
    log "🌐 Deploying static frontend to Vercel..."
    mkdir -p frontend
    cp "$FRONTEND_PATH" frontend/index.html
    pushd frontend
    vercel --prod --confirm --name "$VERCEL_PROJECT_NAME"
    popd
    log "🌍 Visit: https://$VERCEL_PROJECT_NAME.vercel.app"
  else
    log "⚠️ Vercel CLI not found. Skipping frontend deploy."
    log "Install via: npm i -g vercel"
  fi

  send_slack_notification ":white_check_mark: *$APP_NAME deployed successfully!*"
  send_email_notification "$APP_NAME Deployment" "$APP_NAME was deployed successfully at $(date).\nCommit: $LAST_COMMIT"
  log "✅ Deployment complete."
}

# Load env variables at the start
load_env

if [[ "$1" == "--watch" ]]; then
  deploy
  redeploy_on_change
else
  deploy
fi

```
---
## USAGE

```
make deploy     # Deploy once
make watch      # Auto-redeploy on file changes
make logs       # View logs
make stop       # Stop containers
```
