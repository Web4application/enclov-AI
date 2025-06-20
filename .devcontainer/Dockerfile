FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install global tools if needed (optional)
RUN npm install -g serve

# Set up Python packages early to cache them in Docker layer
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt
