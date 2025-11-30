# -----------------------------------------
# 1. Base Image
# -----------------------------------------
FROM python:3.10-slim

# Avoid Python writing .pyc files and ensure output is flushed
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# -----------------------------------------
# 2. System Dependencies
# -----------------------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------
# 3. Work Directory
# -----------------------------------------
WORKDIR /app

# -----------------------------------------
# 4. Copy Project Files
# -----------------------------------------
COPY . /app

# -----------------------------------------
# 5. Install Python Dependencies
# -----------------------------------------
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# -----------------------------------------
# 6. Command to Run Backtester (Default)
# -----------------------------------------
# Example usage:
#   docker run backtester python -m src.backtester
CMD ["python3", "src/backtester.py"]
