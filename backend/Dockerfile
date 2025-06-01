# Use official Ubuntu base image
FROM ubuntu:18.04

# Set working directory inside container
WORKDIR /app

# Install curl, nodejs, npm dependencies
RUN apt-get update && apt-get install -y curl nodejs npm

# Use NodeSource for newer Node.js (optional)
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

# Copy project files into container
COPY . .

# Install npm dependencies
RUN npm install

# Set environment variable for ConfigCat auth key (to be passed at build or runtime)
ARG CONFIGCAT_AUTH_KEY
ENV CONFIGCAT_AUTH_KEY=$CONFIGCAT_AUTH_KEY

# Run your ConfigCat environment creation command
RUN curl "https://api.configcat.com/v1/products/dcd53ddb-8104-4e48-8cc0-5df1088c6113/environments" \
    -X POST \
    -u $CONFIGCAT_AUTH_KEY: \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"webapp.io-$JOB_ID\"}"

# Expose port 3000 for React dev server or production server
EXPOSE 3000

# Set environment variable for React ConfigCat env at runtime (pass JOB_ID at build or runtime)
ENV REACT_CONFIGCAT_ENV="layerci-$JOB_ID"

# Start React app (run dev server or build+serve in prod)
CMD ["npm", "start"]
