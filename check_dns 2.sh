#!/bin/bash

echo "🔍 DNS Status Checker for med-menu.com"
echo "======================================"

CURRENT_IP=$(curl -s http://checkip.amazonaws.com)
echo "Current server IP: $CURRENT_IP"
echo

# Check DNS resolution
echo "DNS Resolution:"
echo "---------------"
DOMAIN_IP=$(nslookup med-menu.com | grep -A1 "Non-authoritative answer:" | grep "Address:" | awk '{print $2}')
WWW_DOMAIN_IP=$(nslookup www.med-menu.com | grep -A1 "Non-authoritative answer:" | grep "Address:" | awk '{print $2}')

echo "med-menu.com resolves to: $DOMAIN_IP"
echo "www.med-menu.com resolves to: $WWW_DOMAIN_IP"
echo

# Check if DNS is correct
if [ "$DOMAIN_IP" = "$CURRENT_IP" ] && [ "$WWW_DOMAIN_IP" = "$CURRENT_IP" ]; then
    echo "✅ DNS is correctly configured!"
    echo "You can now run: sudo ./setup_https.sh"
else
    echo "❌ DNS still needs to be updated."
    echo "Required: Both domains should point to $CURRENT_IP"
    echo
    echo "Please update your DNS records:"
    echo "  med-menu.com     A    $CURRENT_IP"
    echo "  www.med-menu.com A    $CURRENT_IP"
    echo
    echo "DNS propagation can take 5-30 minutes."
fi

echo
echo "Run this script again after updating DNS to check status."
