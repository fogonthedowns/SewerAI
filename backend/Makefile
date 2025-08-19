.PHONY: install test run clean setup venv help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default target - show help when just typing 'make'
.DEFAULT_GOAL := help

# Help target - shows all available commands
help:
	@echo "Available Commands:"
	@echo ""
	@echo "  make setup    - Complete setup (clean + create venv + install deps)"
	@echo "  make venv     - Create virtual environment only"
	@echo "  make install  - Install dependencies in venv"
	@echo "  make test     - Test S3 streaming connection"
	@echo "  make run      - Start Flask backend server"
	@echo "  make clean    - Clean up venv and cache files"
	@echo "  make help     - Show this help message"
	@echo ""

# Create virtual environment
venv:
	@echo "Creating Python virtual environment..."
	python3 -m venv $(VENV)
	@echo "✅ Virtual environment created"

# Install Python dependencies in venv
install: venv
	@echo "Installing Python dependencies in virtual environment..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed in venv"

# Test S3 streaming using venv
test: install
	@echo "Testing S3 connection and data streaming..."
	$(PYTHON) test_streaming.py

# Run the Flask app using venv
run: install
	@echo "Starting Flask backend with virtual environment..."
	@echo "API will be available at http://localhost:5001"
	$(PYTHON) src/app.py

# Setup everything from scratch
setup: clean install
	@echo "✅ Complete setup finished"

# Clean up including venv
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf src/__pycache__
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "✅ Cleaned up virtual environment and cache files"