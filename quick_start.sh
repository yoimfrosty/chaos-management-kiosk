#!/bin/bash

# Ocean City Hemp Kiosk - Quick Start Script
# Use this script when the environment is already set up and you just want to start the server

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🌿 Ocean City Hemp Kiosk - Quick Start${NC}"
echo -e "${BLUE}=====================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Please run ./start_app.sh first.${NC}"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export DEBUG=True
export DJANGO_SETTINGS_MODULE=OceanCityKiosk.settings

# Quick status check
echo -e "${GREEN}✓${NC} Environment activated"
echo -e "${GREEN}✓${NC} Starting server..."
echo ""
echo -e "${BLUE}Access at: ${GREEN}http://localhost:8000/${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Start server
python manage.py runserver 0.0.0.0:8000
