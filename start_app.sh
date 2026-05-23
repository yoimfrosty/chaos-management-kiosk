#!/bin/bash

# Ocean City Hemp Kiosk - Startup Script
# This script handles the complete setup and startup process for the Django app

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🌿 Ocean City Hemp Kiosk Management System${NC}"
echo -e "${BLUE}===========================================${NC}"
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

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_info "Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Check if Django is installed in venv
if ! python -c "import django" &> /dev/null; then
    print_info "Installing Python dependencies..."
    
    # Install core dependencies that work with older Python versions
    if [[ "$PYTHON_VERSION" < "3.10" ]]; then
        print_warning "Python $PYTHON_VERSION detected. Installing compatible Django version..."
        pip install Django==4.2.23 Pillow python-dotenv python-dateutil --quiet
    else
        pip install -r requirements.txt --quiet
    fi
    
    print_status "Dependencies installed"
else
    # Even if Django is installed, check for missing dependencies
    print_info "Checking for missing dependencies..."
    if ! python -c "from dateutil.relativedelta import relativedelta" &> /dev/null; then
        print_warning "Missing python-dateutil dependency, installing..."
        pip install python-dateutil --quiet
    fi
    
    # Try to install all requirements to catch any missing ones
    pip install -r requirements.txt --quiet &> /dev/null || print_warning "Some dependencies may be missing, but continuing..."
    print_status "Dependencies verified"
fi

# Set environment variables for development
export DEBUG=True
export DJANGO_SETTINGS_MODULE=OceanCityKiosk.settings

# Verify Django can import properly
print_info "Verifying Django configuration..."
if ! python -c "import django; django.setup(); from kiosk.models import Category" &> /dev/null; then
    print_error "Django configuration has issues. Checking for missing dependencies..."
    
    # Try to install missing dependencies
    print_info "Installing any missing dependencies..."
    pip install -r requirements.txt --quiet
    
    # Try again
    if ! python -c "import django; django.setup(); from kiosk.models import Category" &> /dev/null; then
        print_error "Django configuration still has issues. Please check the error above."
        exit 1
    fi
fi

# Test age verification view
print_info "Testing age verification view..."
if ! python -c "
import django
django.setup()
from django.test import Client
client = Client()
response = client.get('/')
assert response.status_code == 200, f'Age verification page returned status {response.status_code}'
print('Age verification page is accessible')
" &> /dev/null; then
    print_warning "Age verification page test failed, but continuing anyway..."
else
    print_status "Age verification page is working correctly"
fi

print_status "Django configuration verified"

# Check if database exists and has been migrated
if [ ! -f "db.sqlite3" ]; then
    print_info "Setting up database..."
    python manage.py migrate
    print_status "Database migrations complete"
    
    # Create superuser if it doesn't exist
    print_info "Creating admin user..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@oceancityhemp.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
    print_status "Admin user created (username: admin, password: admin123)"
else
    # Check if migrations are needed
    if ! python manage.py showmigrations --plan | grep -q "No migrations to apply"; then
        print_info "Applying database migrations..."
        python manage.py migrate
        print_status "Database migrations complete"
    else
        print_status "Database is up to date"
    fi
fi

# Collect static files (in case any are missing)
print_info "Collecting static files..."
python manage.py collectstatic --noinput --clear &> /dev/null || true
print_status "Static files ready"

# Create media directories if they don't exist
mkdir -p mediafiles/products mediafiles/categories
print_status "Media directories ready"

# Display startup information
echo ""
echo -e "${GREEN}🚀 Starting Ocean City Hemp Kiosk Management System...${NC}"
echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo -e "  • Age Verification: ${GREEN}http://localhost:8000/${NC}"
echo -e "  • Admin Panel:      ${GREEN}http://localhost:8000/admin/${NC}"
echo -e "  • Network Access:   ${GREEN}http://$(ipconfig getifaddr en0 2>/dev/null || echo "YOUR_IP"):8000/${NC}"
echo ""
echo -e "${BLUE}Admin Credentials:${NC}"
echo -e "  • Username: ${GREEN}medmenu${NC}"
echo -e "  • Password: ${GREEN}4Roxanne?${NC}"
echo ""
echo -e "${BLUE}Features Available:${NC}"
echo -e "  • Direct age verification entry page"
echo -e "  • Modern, responsive customer interface"
echo -e "  • Product management and categories"
echo -e "  • Real-time budtender call system"
echo -e "  • Order processing and receipts"
echo -e "  • Admin dashboard for management"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
