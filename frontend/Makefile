.PHONY: help build run clean install start dev

# Default target - show help when just typing 'make'
.DEFAULT_GOAL := help

# Help target - shows all available commands
help:
	@echo "Frontend Commands:"
	@echo ""
	@echo "  make install  - Install Node.js dependencies"
	@echo "  make build    - Build for production"
	@echo "  make run      - Start development server"
	@echo "  make start    - Start development server (alias for run)"
	@echo "  make dev      - Start development server with auto-reload"
	@echo "  make clean    - Clean up build files and dependencies"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Quick start: make install && make run"

# Install dependencies
install:
	@echo "Installing frontend dependencies..."
	npm install
	@echo "✅ Frontend dependencies installed"

# Build for production
build: install
	@echo "Building React app for production..."
	npm run build
	@echo "✅ Production build complete in build/ directory"

# Start development server
run: install
	@echo "Starting React development server..."
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Make sure Flask backend is running on http://localhost:5001"
	npm start

# Alias for run
start: run

# Development mode (same as run for React)
dev: run

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf node_modules
	rm -rf build
	rm -rf package-lock.json
	@echo "✅ Cleaned up frontend files"