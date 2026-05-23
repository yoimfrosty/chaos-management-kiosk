#!/usr/bin/env python3

import requests
import re

# Test age verification
print("Testing age verification...")

session = requests.Session()

# Get the age verification page
response = session.get("http://localhost:8000/verify-age/")
print(f"GET /verify-age/ -> {response.status_code}")

# Extract CSRF token
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
if csrf_match:
    csrf_token = csrf_match.group(1)
    print(f"CSRF token: {csrf_token[:10]}...")
    
    # Submit age verification
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'is_21_plus': 'on'
    }
    
    response = session.post("http://localhost:8000/verify-age/", data=data)
    print(f"POST /verify-age/ -> {response.status_code}")
    print(f"Final URL: {response.url}")
    
    # Check session cookies
    print("Session cookies:")
    for cookie in session.cookies:
        print(f"  {cookie.name}={cookie.value}")
    
    # Test if age verification worked
    test_response = session.get("http://localhost:8000/products/")
    print(f"GET /products/ -> {test_response.status_code}")
    
    if test_response.status_code == 200:
        print("✔ Age verification successful!")
    elif test_response.status_code == 302:
        print("❌ Still redirecting - age verification failed")
    
else:
    print("❌ Could not find CSRF token")
