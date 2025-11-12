.PHONY: help install test test-ui test-api test-performance test-security test-accessibility test-visual test-smoke lint format clean coverage report

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
PLAYWRIGHT := playwright

help: ## Show this help message
	@echo "E-Commerce Test Suite - Available Commands"
	@echo "==========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install
	@echo "✅ Installation complete!"

install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	$(PIP) install -r requirements.txt
	$(PIP) install black isort pylint mypy pytest-cov
	$(PLAYWRIGHT) install --with-deps
	@echo "✅ Development setup complete!"

test: ## Run all tests
	@echo "Running all tests..."
	$(PYTEST) -v

test-ui: ## Run UI tests only
	@echo "Running UI tests..."
	$(PYTEST) ui_tests/ -v

test-api: ## Run API tests only
	@echo "Running API tests..."
	$(PYTEST) api_tests/ -v

test-performance: ## Run performance tests
	@echo "Running performance tests..."
	$(PYTEST) performance/tests/ -v

test-security: ## Run security tests
	@echo "Running security tests..."
	$(PYTEST) security/tests/ -v

test-accessibility: ## Run accessibility tests
	@echo "Running accessibility tests..."
	$(PYTEST) accessibility/tests/ -v

test-visual: ## Run visual regression tests
	@echo "Running visual regression tests..."
	$(PYTEST) visual/tests/ -v

test-smoke: ## Run smoke tests only
	@echo "Running smoke tests..."
	$(PYTEST) -m smoke -v

test-parallel: ## Run tests in parallel
	@echo "Running tests in parallel..."
	$(PYTEST) -n 4 -v

lint: ## Run code linting
	@echo "Running linters..."
	pylint **/*.py || true
	@echo "✅ Linting complete!"

format: ## Format code with Black and isort
	@echo "Formatting code..."
	black .
	isort .
	@echo "✅ Code formatted!"

typecheck: ## Run type checking with mypy
	@echo "Running type checker..."
	mypy . --ignore-missing-imports || true
	@echo "✅ Type checking complete!"

quality: format lint typecheck ## Run all code quality checks
	@echo "✅ All quality checks complete!"

coverage: ## Run tests with coverage
	@echo "Running tests with coverage..."
	$(PYTEST) --cov=. --cov-report=html --cov-report=term
	@echo "✅ Coverage report generated in htmlcov/"

coverage-report: ## Generate and open coverage report
	@echo "Generating coverage report..."
	$(PYTEST) --cov=. --cov-report=html
	open htmlcov/index.html || xdg-open htmlcov/index.html
	@echo "✅ Coverage report opened!"

report: ## Generate HTML test report
	@echo "Generating test report..."
	$(PYTEST) --html=reports/html/report.html --self-contained-html
	@echo "✅ Test report generated!"

clean: ## Clean up generated files
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf reports/html/*
	rm -rf reports/allure/*
	rm -rf visual/diffs/*.png
	rm -rf visual/temp/*.png
	@echo "✅ Cleanup complete!"

clean-all: clean ## Clean everything including baselines
	rm -rf visual/baselines/*.png
	rm -rf logs/*
	@echo "✅ Full cleanup complete!"

setup: install ## Initial setup (alias for install)
	@echo "✅ Setup complete! Run 'make test-smoke' to verify."

run-locust: ## Run Locust load test
	@echo "Starting Locust..."
	locust -f performance/locust/locustfile.py --host https://www.demoblaze.com

ci: quality test ## Run CI pipeline locally
	@echo "Running CI checks..."
	$(PYTEST) -m "not slow" --maxfail=10
	@echo "✅ CI checks passed!"

watch: ## Watch for file changes and run tests
	@echo "Watching for changes..."
	$(PYTEST) -f

serve-report: ## Serve test reports
	@echo "Serving reports on http://localhost:8000"
	cd reports && python -m http.server 8000

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t e-commerce-test-suite .
	@echo "✅ Docker image built!"

docker-run: ## Run tests in Docker
	@echo "Running tests in Docker..."
	docker run --rm e-commerce-test-suite

update-deps: ## Update all dependencies
	@echo "Updating dependencies..."
	$(PIP) install --upgrade -r requirements.txt
	@echo "✅ Dependencies updated!"

check: ## Quick health check
	@echo "Running health check..."
	$(PYTHON) --version
	$(PYTEST) --version
	$(PLAYWRIGHT) --version
	@echo "✅ Environment healthy!"

baseline-update: ## Update visual regression baselines
	@echo "Updating visual baselines..."
	$(PYTEST) visual/tests/ -v
	@echo "✅ Baselines updated!"

baseline-clear: ## Clear all visual baselines
	@echo "Clearing baselines..."
	rm -rf visual/baselines/*.png
	rm -rf visual/diffs/*.png
	@echo "✅ Baselines cleared!"
