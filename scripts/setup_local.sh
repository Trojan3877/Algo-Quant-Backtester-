#!/usr/bin/env bash
# scripts/setup_local.sh
# Author: Corey Leath

set -e

echo "1. Copy .env.example to .env and fill in variables"
cp .env.example .env

echo "2. Install Python dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "3. Initialize DVC and pull data"
dvc init --no-scm || true
dvc remote add -d origin ${DVC_REMOTE_URL}
dvc pull

echo "4. Start local services with Docker Compose"
docker-compose up -d --build

echo "5. Start Airflow (if used)"
# Uncomment if using Airflow:
# (cd airflow && docker-compose up -d)

echo "6. (Optional) Start MLflow"
# (cd mlflow && docker-compose up -d)

echo "Setup complete! You can now run 'make backtest' or 'make serve'."


chmod +x scripts/setup_local.sh
git add scripts/setup_local.sh
git commit -m "Add setup_local.sh for local environment bootstrap"
git push
