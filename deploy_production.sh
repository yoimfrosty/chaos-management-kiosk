#!/bin/bash

# Ocean City Hemp Kiosk - Production Deployment Script
# This script sets up the production environment with nginx and gunicorn

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🌿 Ocean City Hemp Kiosk - Production Deployment${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if running as root for some operations
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons."
   exit 1
fi

print_info "Setting up production environment..."

# Create necessary directories
print_info "Creating log directories..."
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/run/gunicorn
print_status "Log directories created"

# Set up environment variables
print_info "Loading production environment..."
export DJANGO_SETTINGS_MODULE=OceanCityKiosk.settings_production
if [ -f ".env.production" ]; then
    export $(grep -v '^#' .env.production | xargs)
fi

# Collect static files
print_info "Collecting static files..."
python3 manage.py collectstatic --noinput --clear
print_status "Static files collected"

# Run database migrations
print_info "Running database migrations..."
python3 manage.py migrate
print_status "Database migrations complete"

# Create superuser if it doesn't exist
print_info "Setting up admin user..."
python3 manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@oceancityhemp.com', 'admin123')
    print("Admin user created")
else:
    print("Admin user already exists")
EOF
print_status "Admin user configured"

# Install systemd service
print_info "Installing systemd service..."
sudo cp ocean-city-hemp-kiosk.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ocean-city-hemp-kiosk
print_status "Systemd service installed"

# Configure nginx
print_info "Configuring nginx..."
sudo cp nginx-ocean-city-hemp-kiosk.conf /etc/nginx/sites-available/ocean-city-hemp-kiosk
sudo ln -sf /etc/nginx/sites-available/ocean-city-hemp-kiosk /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
print_status "Nginx configured"

# Test nginx configuration
print_info "Testing nginx configuration..."
sudo nginx -t
print_status "Nginx configuration is valid"

# Set proper permissions
print_info "Setting file permissions..."
sudo chown -R ubuntu:ubuntu /home/ubuntu/chaos-magement
chmod +x gunicorn.conf.py
print_status "File permissions set"

# Start services
print_info "Starting services..."
sudo systemctl restart ocean-city-hemp-kiosk
sudo systemctl restart nginx
print_status "Services started"

# Check service status
print_info "Checking service status..."
sleep 3
if systemctl is-active --quiet ocean-city-hemp-kiosk; then
    print_status "Ocean City Hemp Kiosk service is running"
else
    print_error "Ocean City Hemp Kiosk service failed to start"
    sudo systemctl status ocean-city-hemp-kiosk
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_status "Nginx service is running"
else
    print_error "Nginx service failed to start"
    sudo systemctl status nginx
    exit 1
fi

# Display deployment information
echo ""
echo -e "${GREEN}🚀 Production Deployment Complete!${NC}"
echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo -e "  • Main Application: ${GREEN}http://localhost/${NC}"
echo -e "  • Admin Panel:      ${GREEN}http://localhost/admin/${NC}"
echo -e "  • Public IP:        ${GREEN}http://3.88.244.164/${NC}"
echo -e "  • Your Domain:      ${GREEN}http://your-domain.com/${NC} (when DNS is configured)"
echo ""
echo -e "${BLUE}Admin Credentials:${NC}"
echo -e "  • Username: ${GREEN}admin${NC}"
echo -e "  • Password: ${GREEN}admin123${NC}"
echo ""
echo -e "${BLUE}Service Management:${NC}"
echo -e "  • Start:   ${YELLOW}sudo systemctl start ocean-city-hemp-kiosk${NC}"
echo -e "  • Stop:    ${YELLOW}sudo systemctl stop ocean-city-hemp-kiosk${NC}"
echo -e "  • Restart: ${YELLOW}sudo systemctl restart ocean-city-hemp-kiosk${NC}"
echo -e "  • Status:  ${YELLOW}sudo systemctl status ocean-city-hemp-kiosk${NC}"
echo -e "  • Logs:    ${YELLOW}sudo journalctl -u ocean-city-hemp-kiosk -f${NC}"
echo ""
echo -e "${BLUE}Nginx Management:${NC}"
echo -e "  • Start:   ${YELLOW}sudo systemctl start nginx${NC}"
echo -e "  • Stop:    ${YELLOW}sudo systemctl stop nginx${NC}"
echo -e "  • Restart: ${YELLOW}sudo systemctl restart nginx${NC}"
echo -e "  • Status:  ${YELLOW}sudo systemctl status nginx${NC}"
echo -e "  • Test:    ${YELLOW}sudo nginx -t${NC}"
echo ""
echo -e "${YELLOW}Note: Remember to update your domain DNS to point to your server's IP address.${NC}"
echo -e "${YELLOW}For HTTPS, consider setting up Let's Encrypt with certbot.${NC}"
echo ""
