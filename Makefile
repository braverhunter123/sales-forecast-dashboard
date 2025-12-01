# Makefile for Sales Forecasting Dashboard

# Variables
PYTHON = python3
PIP = pip3
REQUIREMENTS = requirements.txt

# Default target
.PHONY: help
help:
	@echo "Sales Forecasting Dashboard - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install     Install dependencies"
	@echo "  make dashboard   Run the Streamlit dashboard"
	@echo "  make pipeline    Run the sales forecasting pipeline"
	@echo "  make test        Run unit tests"
	@echo "  make clean       Clean temporary files"
	@echo "  make help        Show this help message"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r $(REQUIREMENTS)

# Run the dashboard
.PHONY: dashboard
dashboard:
	$(PYTHON) run.py dashboard

# Run the pipeline
.PHONY: pipeline
pipeline:
	$(PYTHON) run.py pipeline

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest tests/

# Clean temporary files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

# Setup development environment
.PHONY: setup
setup: install
	@echo "Development environment setup complete!"

# Run all checks
.PHONY: check
check: test
	@echo "All checks passed!"