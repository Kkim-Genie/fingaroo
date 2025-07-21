FROM python:3.12-slim

WORKDIR /app

# Copy necessary files
COPY apps/ai/pyproject.toml .
COPY apps/ai/main.py .
COPY apps/ai/app app/


# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies using uv pip install
RUN uv sync

# Install Playwright
RUN pip install playwright
RUN playwright install --with-deps

# Expose the port
EXPOSE 8001

# Command to run the application
CMD ["uv", "run", "main.py"] 