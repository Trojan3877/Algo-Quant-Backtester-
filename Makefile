# Makefile for AlgoQuant Backtester & Signal Engine

.PHONY: deps lint test backtest serve deploy clean

# Install Python dependencies
deps:
	pip install -r requirements.txt

# Lint Python code
lint:
	flake8 src/

# Run unit tests
test:
	pytest --maxfail=1 --disable-warnings -q

# Run the backtester module
backtest:
	python src/backtest/backtest.py --config configs/backtest.yaml

# Start the FastAPI signal service
serve:
	uvicorn src.serve.app:app --reload --port 8000

# Deploy to Kubernetes via kubectl (assumes context/config set)
deploy:
	kubectl apply -f k8s/

# Clean up caches and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + && \
	rm -rf data/processed models/*.pkl

git add Makefile
git commit -m "Add Makefile with common tasks"
git push
