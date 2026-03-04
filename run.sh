#!/bin/bash
set -e

echo "Starting the Travel Insurance Analyzer (Producer -> Kafka -> Consumer)..."

# Stop and remove any existing containers to start from scratch
docker compose down

# Build the images and start the containers
docker compose up --build
