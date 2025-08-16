# Dev image with Python + Playwright browsers preinstalled
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Set workdir
WORKDIR /app

# System deps (optional)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip &&     pip install --no-cache-dir -r /app/requirements.txt &&     pip install --no-cache-dir pytest ruff

# Copy source
COPY . /app

# Playwright browsers already installed in base image
# If you used a plain Python image, you'd need: RUN playwright install

# Default environment (override via docker-compose or env)
ENV OPENAI_API_KEY=""
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Entry point: run orchestrator
CMD ["python", "main.py"]
