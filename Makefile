.PHONY: help up down logs clean build train ingest test

# Default target
help:
	@echo "Available commands:"
	@echo "  make up        - Start all services with Docker Compose"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - View logs from all services"
	@echo "  make clean     - Clean up containers and volumes"
	@echo "  make build     - Build all Docker images"
	@echo "  make train     - Train ML models"
	@echo "  make ingest    - Start data ingestion"
	@echo "  make test      - Run tests"
	@echo "  make setup     - Setup environment"

# Setup environment
setup:
	@echo "Setting up environment..."
	@cp .env.example .env || echo ".env already exists"
	@echo "Please edit .env file with your API keys"

# Start all services
up:
	@echo "Starting all services..."
	docker-compose up --build -d

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up
clean:
	@echo "Cleaning up..."
	docker-compose down -v
	docker system prune -f

# Build all images
build:
	@echo "Building all images..."
	docker-compose build

# Train models
train:
	@echo "Training ML models..."
	cd congestion_detector && python train.py

# Start data ingestion
ingest:
	@echo "Starting data ingestion..."
	cd ingestion && python gps_producer.py &
	cd ingestion && python weather_producer.py &
	cd ingestion && python events_producer.py &

# Run tests
test:
	@echo "Running tests..."
	@echo "Tests not implemented yet"

# Development helpers
dev-up:
	@echo "Starting development environment..."
	docker-compose up kafka redis zookeeper -d
	@echo "Kafka and Redis started. Run individual services locally."

restart:
	@echo "Restarting services..."
	docker-compose restart

status:
	@echo "Service status:"
	docker-compose ps 