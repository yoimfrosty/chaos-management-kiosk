#!/usr/bin/env python3
"""
Test template rendering by creating a minimal view
"""

import os
import sys
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

import django
django.setup()

from django.test import Client
from django.urls import reverse

def test_template_direct():
    """Test template rendering directly with Django test client"""
    print("🔍 Testing Template Rendering Directly")
    print("="*45)
    
    try:
        # Create Django test client
        client = Client()
        
        # Set age verification in session
        session = client.session
        session['is_21_plus'] = True
        session.save()
        
        print("1. Testing simple receipt template...")
        
        # Test the simple receipt view
        response = client.get('/test-receipt/1/')
        
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            if len(response.content) > 0:
                content = response.content.decode('utf-8')
                print(f"   ✔ Template rendered successfully!")
                print(f"   📄 Content preview: {content[:200]}...")
                
                if "OCEAN CITY KIOSK" in content:
                    print("   ✔ Business name found")
                if "<style>" in content:
                    print("   ✔ CSS styling found")
                if "PAYMENT REQUIRED" in content:
                    print("   ✔ Payment status found")
                    
                return True
            else:
                print("   ❌ Empty content - template rendering issue")
                
                # Check for template errors
                if hasattr(response, 'templates') and response.templates:
                    print(f"   📋 Templates used: {[t.name for t in response.templates]}")
                else:
                    print("   ❌ No templates found")
                    
                if hasattr(response, 'context') and response.context:
                    print(f"   📊 Context keys: {list(response.context.keys())}")
                else:
                    print("   ❌ No context found")
                    
        elif response.status_code == 302:
            print(f"   ❌ Redirected to: {response.url}")
        else:
            print(f"   ❌ Error status: {response.status_code}")
            
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_template_direct()
    if success:
        print(f"\n🎉 Template rendering works with Django client!")
    else:
        print(f"\n❌ Template rendering issue confirmed")
