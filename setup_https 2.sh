#!/bin/bash
set -e

echo "🔒 Ocean City Hemp Kiosk - HTTPS Setup Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check DNS resolution
check_dns() {
    echo -e "${YELLOW}Checking DNS resolution...${NC}"
    
    CURRENT_IP=$(curl -s http://checkip.amazonaws.com)
    echo "Current server IP: $CURRENT_IP"
    
    DOMAIN_IP=$(nslookup med-menu.com | grep -A1 "Non-authoritative answer:" | grep "Address:" | awk '{print $2}')
    WWW_DOMAIN_IP=$(nslookup www.med-menu.com | grep -A1 "Non-authoritative answer:" | grep "Address:" | awk '{print $2}')
    
    echo "med-menu.com resolves to: $DOMAIN_IP"
    echo "www.med-menu.com resolves to: $WWW_DOMAIN_IP"
    
    if [ "$DOMAIN_IP" != "$CURRENT_IP" ] || [ "$WWW_DOMAIN_IP" != "$CURRENT_IP" ]; then
        echo -e "${RED}❌ DNS not properly configured!${NC}"
        echo "Please update your DNS records to point both domains to: $CURRENT_IP"
        echo "Current DNS points to: $DOMAIN_IP"
        return 1
    else
        echo -e "${GREEN}✅ DNS properly configured!${NC}"
        return 0
    fi
}

# Function to test HTTP access
test_http_access() {
    echo -e "${YELLOW}Testing HTTP access...${NC}"
    
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://med-menu.com)
    WWW_HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://www.med-menu.com)
    
    echo "HTTP status for med-menu.com: $HTTP_STATUS"
    echo "HTTP status for www.med-menu.com: $WWW_HTTP_STATUS"
    
    if [ "$HTTP_STATUS" = "200" ] && [ "$WWW_HTTP_STATUS" = "200" ]; then
        echo -e "${GREEN}✅ HTTP access working!${NC}"
        return 0
    else
        echo -e "${RED}❌ HTTP access not working properly${NC}"
        return 1
    fi
}

# Function to setup SSL with Let's Encrypt
setup_ssl() {
    echo -e "${YELLOW}Setting up SSL with Let's Encrypt...${NC}"
    
    # Run certbot
    sudo certbot --nginx -d med-menu.com -d www.med-menu.com --non-interactive --agree-tos --email dibya.ddk@gmail.com
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SSL certificates obtained successfully!${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to obtain SSL certificates${NC}"
        return 1
    fi
}

# Function to enable HTTPS in Django settings
enable_django_https() {
    echo -e "${YELLOW}Enabling HTTPS in Django settings...${NC}"
    
    # Update .env.production to enable HTTPS
    sed -i 's/HTTPS_ENABLED=false/HTTPS_ENABLED=true/' /home/ubuntu/chaos-magement/.env.production
    
    echo -e "${GREEN}✅ Django HTTPS settings enabled${NC}"
}

# Function to restart services
restart_services() {
    echo -e "${YELLOW}Restarting services...${NC}"
    
    sudo systemctl restart ocean-city-hemp-kiosk
    sudo systemctl reload nginx
    
    echo -e "${GREEN}✅ Services restarted${NC}"
}

# Function to test HTTPS access
test_https_access() {
    echo -e "${YELLOW}Testing HTTPS access...${NC}"
    
    sleep 5  # Wait for services to fully restart
    
    HTTPS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://med-menu.com)
    WWW_HTTPS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://www.med-menu.com)
    
    echo "HTTPS status for med-menu.com: $HTTPS_STATUS"
    echo "HTTPS status for www.med-menu.com: $WWW_HTTPS_STATUS"
    
    if [ "$HTTPS_STATUS" = "200" ] && [ "$WWW_HTTPS_STATUS" = "200" ]; then
        echo -e "${GREEN}✅ HTTPS access working!${NC}"
        return 0
    else
        echo -e "${RED}❌ HTTPS access not working properly${NC}"
        return 1
    fi
}

# Function to setup auto-renewal
setup_auto_renewal() {
    echo -e "${YELLOW}Setting up SSL certificate auto-renewal...${NC}"
    
    # Test renewal
    sudo certbot renew --dry-run
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Auto-renewal configured successfully!${NC}"
        echo "Certificates will auto-renew via systemd timer."
    else
        echo -e "${RED}❌ Auto-renewal test failed${NC}"
    fi
}

# Main execution
echo "Starting HTTPS setup process..."
echo

# Step 1: Check DNS
if ! check_dns; then
    echo -e "${RED}Stopping setup - DNS needs to be fixed first.${NC}"
    exit 1
fi

echo

# Step 2: Test HTTP access
if ! test_http_access; then
    echo -e "${RED}Stopping setup - HTTP access needs to be working first.${NC}"
    exit 1
fi

echo

# Step 3: Setup SSL
if ! setup_ssl; then
    echo -e "${RED}SSL setup failed. Check the logs above.${NC}"
    exit 1
fi

echo

# Step 4: Enable HTTPS in Django
enable_django_https

echo

# Step 5: Restart services
restart_services

echo

# Step 6: Test HTTPS access
if ! test_https_access; then
    echo -e "${RED}HTTPS setup completed but testing failed. Check configuration.${NC}"
fi

echo

# Step 7: Setup auto-renewal
setup_auto_renewal

echo
echo -e "${GREEN}🎉 HTTPS setup completed successfully!${NC}"
echo
echo "Your website is now available at:"
echo "  • https://med-menu.com"
echo "  • https://www.med-menu.com"
echo
echo "SSL certificates will auto-renew every 60 days."
echo "You can check certificate status with: sudo certbot certificates"
