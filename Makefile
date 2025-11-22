.PHONY: help install install-dev test lint format clean docker-build docker-run train evaluate

help:
	@echo "Available commands:"
	@echo "  make install       - Install package and dependencies"
	@echo "  make install-dev   - Install package with dev dependencies"
	@echo "  make test          - Run tests with pytest"
	@echo "  make lint          - Run linters (flake8, mypy)"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Clean temporary files"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make train         - Run training script"
	@echo "  make evaluate      - Run evaluation script"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ --cov=src/text2sql --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/ scripts/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/ scripts/ api/
	isort src/ tests/ scripts/ api/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/

docker-build:
	docker-compose build

docker-run:
	docker-compose up training

train:
	python scripts/train.py --model codellama-7b --dataset spider --method qlora

evaluate:
	python scripts/evaluate.py --model ./outputs --dataset spider --split test

api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
