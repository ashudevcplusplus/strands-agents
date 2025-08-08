SHELL := /bin/bash

.PHONY: help startover clean clean-caches clean-build clean-logs

help:
	@echo "Available targets:"
	@echo "  startover     - Clean caches, build artifacts, and run logs"
	@echo "  clean         - Clean caches and build artifacts"
	@echo "  clean-caches  - Remove Python caches and temporary files"
	@echo "  clean-build   - Remove build/dist and packaging artifacts"
	@echo "  clean-logs    - Remove run logs"

clean-caches:
	@echo "Removing caches and temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@find . -type f -name "*.py[co]" -delete || true
	@find . -type f -name "*~" -delete || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + || true
	@find . -type d -name ".cache" -exec rm -rf {} + || true
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + || true
	@find . -type f -name ".coverage*" -delete || true
	@find . -type f -name ".DS_Store" -delete || true

clean-build:
	@echo "Removing build and packaging artifacts..."
	@rm -rf build/ dist/ .build/ .eggs/ || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + || true

clean-logs:
	@echo "Removing run logs..."
	@rm -rf runlogs/* || true

clean: clean-caches clean-build

startover: clean clean-logs
	@echo "Startover complete."

