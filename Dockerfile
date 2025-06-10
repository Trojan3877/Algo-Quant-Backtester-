# Dockerfile for AlgoQuant Backtester & Signal Engine
# Author: Corey Leath

# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose ports
EXPOSE 8000   # FastAPI
EXPOSE 5000   # (optional) MLflow if included

# Default command: run FastAPI service
CMD ["uvicorn", "src.serve.app:app", "--host", "0.0.0.0", "--port", "8000"]

git add Dockerfile
git commit -m "Add Dockerfile for containerizing service"
git push
