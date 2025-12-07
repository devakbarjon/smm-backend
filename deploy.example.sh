#!/bin/bash

export ENV=production

APP_DIR="/path/to/your/app"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="yourapp"     # systemd service

echo "Starting deployment..."

cd "$APP_DIR" || { echo "Cannot cd to $APP_DIR"; exit 1; }

echo "Pulling latest code..."
git pull origin main || { echo "Git pull failed"; exit 1; }

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate" || { echo "Could not activate venv"; exit 1; }

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt || { echo "Dependency installation failed"; exit 1; }

echo "Running Alembic migrations..."
alembic upgrade head || echo "Alembic not configured — skipping"

echo "Running seeds..."
python -m app.core.seeders.models_seeder || { echo "Seeding failed"; exit 1; }

echo "Restarting service..."
sudo systemctl restart "$SERVICE_NAME" || { echo "Failed to restart service"; exit 1; }

echo "Deployment completed."