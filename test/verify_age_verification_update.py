#!/usr/bin/env python3
"""
Quick verification script for the Ocean City Hemp Kiosk system
Tests that the age verification page works as the homepage
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from kiosk.models import Category, Product

def test_age_verification_homepage():
    """Test that age verification page is accessible as homepage"""
    print("Testing age verification homepage...")
    client = Client()
    
    # Test direct access to homepage
    response = client.get('/')
    if response.status_code != 200:
        print(f"❌ Homepage returned status {response.status_code}")
        return False
    
    # Check that it contains age verification content
    content = response.content.decode()
    if "Age Verification Required" not in content:
        print("❌ Homepage doesn't contain age verification content")
        return False
    
    if "Ocean City Hemp" not in content:
        print("❌ Homepage doesn't contain brand name")
        return False
    
    if "You must be 21 or older" not in content:
        print("❌ Homepage doesn't contain age requirement text")
        return False
    
    print("✅ Age verification homepage is working correctly")
    return True

def test_form_submission():
    """Test age verification form submission"""
    print("Testing age verification form...")
    client = Client()
    
    # Test form submission with valid data
    form_data = {
        'customer_name': 'Test Customer',
        'customer_contact': '555-1234',
        'birthdate': '1990-01-01'
    }
    
    response = client.post('/', form_data, follow=True)
    
    if response.status_code != 200:
        print(f"❌ Form submission returned status {response.status_code}")
        return False
    
    # Check if redirected to product list
    if 'products' not in response.request['PATH_INFO']:
        print("❌ Form submission didn't redirect to products page")
        return False
    
    print("✅ Age verification form submission is working correctly")
    return True

def test_urls():
    """Test that URL routing works correctly"""
    print("Testing URL routing...")
    
    try:
        # Test that age_verification is the root URL
        homepage_url = reverse('kiosk:age_verification')
        if homepage_url != '/':
            print(f"❌ Age verification URL is {homepage_url}, should be /")
            return False
        
        print("✅ URL routing is configured correctly")
        return True
    except Exception as e:
        print(f"❌ URL routing test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🌿 Ocean City Hemp Kiosk - Age Verification Tests")
    print("=" * 50)
    
    tests = [
        test_urls,
        test_age_verification_homepage,
        test_form_submission
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Age verification system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
