# Ocean City Hemp Kiosk - Startup Scripts

This directory contains convenient bash scripts to start the Ocean City Hemp Kiosk Management System.

## Scripts Available

### 🚀 `start_app.sh` - Full Setup & Start
**Use this for first-time setup or when you want a complete environment check.**

```bash
./start_app.sh
```

**What it does:**
- ✅ Checks Python installation and version
- ✅ Creates virtual environment if it doesn't exist
- ✅ Installs/updates all dependencies
- ✅ Runs database migrations
- ✅ Creates admin user (if needed)
- ✅ Collects static files
- ✅ Creates media directories
- ✅ Starts the Django development server
- ✅ Shows all access URLs and credentials

### ⚡ `quick_start.sh` - Fast Restart
**Use this when everything is already set up and you just want to start the server.**

```bash
./quick_start.sh
```

**What it does:**
- ✅ Activates existing virtual environment
- ✅ Sets environment variables
- ✅ Starts the server immediately

## Access Information

Once the server starts, you can access:

| Interface | URL | Purpose |
|-----------|-----|---------|
| **Main Kiosk** | http://localhost:8000/ | Customer interface for browsing and ordering |
| **Admin Panel** | http://localhost:8000/admin/ | Backend management interface |
| **Network Access** | http://YOUR_IP:8000/ | Access from other devices on your network |

### Default Admin Credentials
- **Username:** `admin`
- **Password:** `admin123`

## System Requirements

- **Python:** 3.9+ (Python 3.10+ recommended for latest Django features)
- **OS:** macOS, Linux, or Windows with bash support
- **RAM:** 512MB minimum (2GB+ recommended)
- **Disk:** 100MB minimum for app + dependencies

## Troubleshooting

### If the script fails:

1. **Python not found:**
   ```bash
   # Install Python using Homebrew (macOS)
   brew install python3
   
   # Or download from python.org
   ```

2. **Permission denied:**
   ```bash
   chmod +x start_app.sh
   chmod +x quick_start.sh
   ```

3. **Port 8000 already in use:**
   ```bash
   # Find what's using port 8000
   lsof -i :8000
   
   # Kill the process (replace PID with actual process ID)
   kill -9 PID
   ```

4. **Dependencies fail to install:**
   - Check your internet connection
   - Try running the script again
   - For PostgreSQL issues, the script will use SQLite instead

### Manual Commands

If you prefer to run commands manually:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install Django==4.2.23 Pillow python-dotenv

# Set up database
export DEBUG=True
python manage.py migrate

# Create admin user
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@oceancityhemp.com', 'admin123')" | python manage.py shell

# Start server
python manage.py runserver 0.0.0.0:8000
```

## Features

The Ocean City Hemp Kiosk Management System includes:

### Customer Features
- 🛒 Shopping cart with real-time updates
- 📱 Touch-friendly kiosk interface
- 🔞 Age verification system
- 🏷️ Product categories and search
- 💰 Automatic discounts and special offers
- 📋 Order summary and receipts

### Staff Features
- 🔔 Real-time budtender call system
- 📊 Order management dashboard
- 📦 Product and inventory management
- 👥 Customer service tools
- 📈 Sales reporting

### Admin Features
- 🗃️ Complete product catalog management
- 👤 User and staff management
- 🎯 Category and pricing control
- 📋 Order history and analytics
- ⚙️ System configuration

## Development

To make changes to the app:

1. Edit files in the project directory
2. The server will automatically reload (development mode)
3. For database changes, run: `python manage.py makemigrations && python manage.py migrate`
4. For static file changes, run: `python manage.py collectstatic`

## Security Notes

⚠️ **Important:** The default setup uses development settings with:
- Debug mode enabled
- Default admin credentials
- SQLite database
- No HTTPS

For production deployment, see the `test/DEPLOYMENT.md` file for security hardening instructions.

## Support

For issues or questions about the Ocean City Hemp Kiosk system, check:
- `README.md` - Main project documentation
- `test/` directory - Testing guides and troubleshooting
- Django logs in the terminal output
