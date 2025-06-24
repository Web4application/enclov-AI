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
