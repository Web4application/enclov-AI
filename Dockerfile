# --- Stage 1: Build React frontend ---
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
ARG REACT_APP_CONFIGCAT_ENV
ENV REACT_APP_CONFIGCAT_ENV=$REACT_APP_CONFIGCAT_ENV

RUN npm run build

# --- Stage 2: Install backend dependencies ---
FROM python:3.11-slim AS backend-builder

WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# --- Stage 3: Final image ---
FROM nginx:stable-alpine

# Install Python and Uvicorn for FastAPI
RUN apk add --no-cache python3 py3-pip
RUN pip3 install fastapi uvicorn

# Clean Nginx default content
RUN rm -rf /usr/share/nginx/html/*

# Copy built React frontend
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html

# Copy FastAPI backend
COPY --from=backend-builder /app/backend /app/backend

# Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports
EXPOSE 80 8000

CMD ["/start.sh"]
