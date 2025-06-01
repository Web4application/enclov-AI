# --- Stage 1: Build React frontend ---
FROM node:18-alpine AS frontend-builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
ARG REACT_APP_CONFIGCAT_ENV
ENV REACT_APP_CONFIGCAT_ENV=$REACT_APP_CONFIGCAT_ENV

RUN npm run build

# --- Stage 2: Build backend (FastAPI with Uvicorn) ---
FROM python:3.11-slim AS backend-builder

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# --- Stage 3: Final image, serve React with Nginx and run FastAPI ---
FROM nginx:stable-alpine

# Remove default nginx static content
RUN rm -rf /usr/share/nginx/html/*

# Copy built React files from frontend-builder
COPY --from=frontend-builder /app/build /usr/share/nginx/html

# Copy backend files and virtualenv
COPY --from=backend-builder /app /app

# Copy nginx config to serve React SPA (support client-side routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Install python & dependencies for backend (slim + uvicorn)
RUN apk add --no-cache python3 py3-pip
RUN pip3 install --no-cache-dir fastapi uvicorn

# Expose ports
EXPOSE 80 8000

# Run both Nginx and Uvicorn backend with a small script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
