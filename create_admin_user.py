#!/usr/bin/env python3
"""
Create admin user for managing test products
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Create an admin user if it doesn't exist"""
    username = 'admin'
    email = 'admin@oceancityhemp.com'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"👤 Admin user '{username}' already exists")
        return
    
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print(f"✅ Created admin user:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Admin URL: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    create_admin_user()
