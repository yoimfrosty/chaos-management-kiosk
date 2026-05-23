#!/usr/bin/env python3

import os
import sys
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order

def test_compact_receipt():
    print("🧪 Testing Compact Receipt Implementation")
    print("=" * 50)
    
    # Check for existing orders
    orders = Order.objects.all()
    print(f"📊 Total orders in database: {orders.count()}")
    
    if not orders.exists():
        print("❌ No orders found in database")
        return False
    
    # Test with the first order
    order = orders.first()
    print(f"🔍 Testing with Order ID: {order.id}")
    print(f"📄 Order Number: {order.order_number}")
    
    # Test the receipt URL
    receipt_url = f"http://localhost:8000/print-receipt/{order.id}/"
    print(f"🔗 Testing URL: {receipt_url}")
    
    try:
        response = requests.get(receipt_url, timeout=10)
        print(f"📡 HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            content_length = len(content)
            print(f"📏 Response Length: {content_length} characters")
            
            # Check for compact styling features
            checks = {
                "Compact width (280px)": "max-width: 280px" in content,
                "Modern font family": "Segoe UI" in content,
                "Compact padding": "padding: 14px" in content,
                "Smaller font sizes": "font-size: 12px" in content,
                "Print button": "PRINT RECEIPT" in content,
                "Navigation button": "SHOP MORE" in content,
                "Modern gradient": "linear-gradient" in content,
                "Payment status": "PAYMENT REQUIRED" in content
            }
            
            print("\n✔ Feature Check Results:")
            for feature, passed in checks.items():
                status = "✔" if passed else "❌"
                print(f"   {status} {feature}")
            
            success_count = sum(checks.values())
            total_checks = len(checks)
            
            print(f"\n📈 Overall Score: {success_count}/{total_checks} features implemented")
            
            if success_count >= 6:
                print("🎉 Receipt implementation is working excellently!")
                return True
            else:
                print("⚠️  Some features need attention")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the Django server running?")
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_compact_receipt()
    sys.exit(0 if success else 1)
