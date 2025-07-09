FROM python:3.12-slim

WORKDIR /app

# Copy necessary files
COPY pyproject.toml .
COPY main.py .
COPY app app/

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libatspi2.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies using uv (without creating virtual environment in Docker)
RUN uv pip install --system -r pyproject.toml

# Install Playwright
RUN playwright install --with-deps

# Expose the port
EXPOSE 8001

# Command to run the application
CMD ["python", "main.py"] 