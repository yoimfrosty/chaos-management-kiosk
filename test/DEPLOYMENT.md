# Ocean City Hemp Kiosk - Production Deployment Guide

This guide provides step-by-step instructions for deploying the Ocean City Hemp Kiosk Management System to a production environment.

## Prerequisites

### System Requirements
- Ubuntu 20.04+ / CentOS 8+ / RHEL 8+
- Python 3.9+
- PostgreSQL 12+
- Nginx
- Redis (optional, for caching)
- SSL Certificate
- 4GB+ RAM
- 20GB+ storage

### Required Software Installation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx redis-server -y

# Install PostgreSQL development headers
sudo apt install libpq-dev python3-dev -y
```

## Step 1: Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE oceancityhemp;
CREATE USER kiosk_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE oceancityhemp TO kiosk_user;
ALTER USER kiosk_user CREATEDB;
\q

# Test connection
psql -h localhost -U kiosk_user -d oceancityhemp
```

## Step 2: Application Deployment

```bash
# Create application user
sudo useradd -m -s /bin/bash kiosk
sudo usermod -aG www-data kiosk

# Switch to kiosk user
sudo -u kiosk -i

# Clone repository (or upload files)
git clone https://github.com/your-repo/ocean-city-hemp-kiosk.git
cd ocean-city-hemp-kiosk

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

## Step 3: Environment Configuration

```bash
# Copy production environment template
cp .env.production.template .env.production

# Edit production environment file
nano .env.production

# Set environment variables
export DJANGO_SETTINGS_MODULE=OceanCityKiosk.settings_production
```

### Required Environment Variables

Update `.env.production` with your actual values:

```bash
SECRET_KEY=your-cryptographically-strong-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=oceancityhemp
DB_USER=kiosk_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## Step 4: Django Application Setup

```bash
# Load environment variables
source .env.production
export DJANGO_SETTINGS_MODULE=OceanCityKiosk.settings_production

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Load sample data (optional)
python manage.py populate_sample_data

# Test application
python manage.py check --deploy
```

## Step 5: Gunicorn Configuration

Create systemd service file:

```bash
sudo nano /etc/systemd/system/oceancity-kiosk.service
```

```ini
[Unit]
Description=Ocean City Hemp Kiosk gunicorn daemon
Requires=oceancity-kiosk.socket
After=network.target

[Service]
Type=notify
User=kiosk
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/home/kiosk/ocean-city-hemp-kiosk
ExecStart=/home/kiosk/ocean-city-hemp-kiosk/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn/oceancity-kiosk.sock \
          OceanCityKiosk.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Create socket file:

```bash
sudo nano /etc/systemd/system/oceancity-kiosk.socket
```

```ini
[Unit]
Description=Ocean City Hemp Kiosk gunicorn socket

[Socket]
ListenStream=/run/gunicorn/oceancity-kiosk.sock
SocketUser=www-data
SocketMode=600

[Install]
WantedBy=sockets.target
```

Enable and start services:

```bash
sudo systemctl daemon-reload
sudo systemctl enable oceancity-kiosk.socket
sudo systemctl start oceancity-kiosk.socket
sudo systemctl enable oceancity-kiosk.service
sudo systemctl start oceancity-kiosk.service

# Check status
sudo systemctl status oceancity-kiosk.service
```

## Step 6: Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/oceancity-kiosk
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/your/fullchain.pem;
    ssl_certificate_key /path/to/your/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Static files
    location /static/ {
        alias /home/kiosk/ocean-city-hemp-kiosk/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /home/kiosk/ocean-city-hemp-kiosk/mediafiles/;
        expires 1M;
        add_header Cache-Control "public";
    }

    # Application
    location / {
        proxy_pass http://unix:/run/gunicorn/oceancity-kiosk.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Security: Block access to sensitive files
    location ~ /\. {
        deny all;
    }
    
    location ~ \.(env|log|bak)$ {
        deny all;
    }
}
```

Enable site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/oceancity-kiosk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 7: SSL Certificate Setup

### Using Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

## Step 8: Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'

# Check status
sudo ufw status
```

## Step 9: Monitoring and Maintenance

### Log Rotation

```bash
sudo nano /etc/logrotate.d/oceancity-kiosk
```

```
/home/kiosk/ocean-city-hemp-kiosk/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 kiosk kiosk
    postrotate
        systemctl reload oceancity-kiosk.service
    endscript
}
```

### Database Backup Script

```bash
sudo nano /usr/local/bin/backup-oceancity-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/oceancity-kiosk"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h localhost -U kiosk_user oceancityhemp > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /home/kiosk/ocean-city-hemp-kiosk/mediafiles/

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup-oceancity-db.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-oceancity-db.sh
```

## Step 10: Testing Deployment

### Health Check

```bash
# Test application
curl -I https://yourdomain.com

# Test admin panel
curl -I https://yourdomain.com/admin/

# Check SSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### Performance Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Basic load test
ab -n 100 -c 10 https://yourdomain.com/
```

## Security Checklist

- [ ] Database password is strong and unique
- [ ] SECRET_KEY is cryptographically strong
- [ ] ALLOWED_HOSTS is properly configured
- [ ] SSL certificate is valid and auto-renewing
- [ ] Firewall is configured and active
- [ ] Regular backups are scheduled
- [ ] Application logs are monitored
- [ ] Security headers are configured
- [ ] File permissions are correct
- [ ] Admin credentials are strong

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check gunicorn service: `sudo systemctl status oceancity-kiosk.service`
   - Check socket permissions: `ls -la /run/gunicorn/`

2. **Static Files Not Loading**
   - Run: `python manage.py collectstatic --noinput`
   - Check Nginx configuration

3. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials in .env.production

4. **SSL Certificate Issues**
   - Run: `sudo certbot certificates`
   - Check certificate expiry

### Log Locations

- Application logs: `/home/kiosk/ocean-city-hemp-kiosk/logs/`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`
- Gunicorn logs: `sudo journalctl -u oceancity-kiosk.service`

## Support

For deployment issues or questions, refer to:
- Django deployment documentation
- Nginx documentation
- PostgreSQL documentation
- Application README.md
