#!/usr/bin/env python3
"""
Simple verification script to check if the page loads and contains key elements
"""

import requests

def test_simple():
    try:
        response = requests.get('http://127.0.0.1:8000/products/')
        print(f"Status Code: {response.status_code}")
        
        content = response.text
        
        # Check for key elements
        checks = [
            ('category-nav', 'Category Navigation'),
            ('products-title', 'Products Title'),
            ('action-btn cart', 'Your Items Button'),
            ('action-btn order-number', 'Order Number Button'),
            ('#0ea5e9', 'Blue Color for Your Items'),
            ('#f59e0b', 'Orange Color for Order#'),
            ('color: #1f2937', 'Dark Text Color'),
        ]
        
        for check, name in checks:
            if check in content:
                print(f"✅ {name} found")
            else:
                print(f"❌ {name} NOT found")
                
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_simple()
