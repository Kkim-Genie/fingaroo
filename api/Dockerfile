FROM python:3.12-slim

WORKDIR /app

# Copy necessary files
COPY pyproject.toml .
COPY main.py .
COPY app app/


# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies using uv pip install
RUN uv sync

# Install Playwright
RUN pip install playwright
RUN playwright install --with-deps

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uv", "run", "main.py"]