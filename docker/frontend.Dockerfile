FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY ./frontend/package.json ./frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy application code
COPY ./frontend .

# NOTE: Running as root in development for volume permission compatibility
# For production, create proper non-root user with matching UID/GID

# Expose port
EXPOSE 3000

# Command to run the application
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
