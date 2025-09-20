#!/bin/bash

echo "Setting up Student Services Website development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please review and update .env file with your configuration."
fi

# Build and start containers
echo "Building and starting Docker containers..."
docker-compose up -d --build

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "Running database migrations..."
docker-compose exec -T backend python manage.py migrate

# Install frontend dependencies
echo "Installing frontend dependencies..."
docker-compose exec -T frontend npm install

echo "Setup complete!"
echo ""
echo "Services are now running:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/api/docs/"
echo "  Django Admin: http://localhost:8000/admin/"
echo ""
echo "To create a superuser, run:"
echo "  docker-compose exec backend python manage.py createsuperuser"
echo ""
echo "To stop the services, run:"
echo "  docker-compose down"