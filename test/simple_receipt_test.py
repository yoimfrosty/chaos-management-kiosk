#!/usr/bin/env python3
"""
Simple test to check receipt template content
"""

import requests
import time

def test_receipt_simple():
    """Simple test of receipt page"""
    print("🔍 Simple Receipt Test")
    print("="*30)
    
    try:
        # Wait for server to start
        time.sleep(2)
        
        # Test server accessibility
        response = requests.get("http://localhost:8000", timeout=5)
        print(f"✔ Server accessible: {response.status_code}")
        
        # Try to access an existing receipt
        # Let's test with different order IDs
        for order_id in [1, 2, 3, 4, 5]:
            try:
                response = requests.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=5)
                print(f"📄 Order {order_id}: Status {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    print(f"   Content length: {len(content)} characters")
                    
                    # Check for key elements
                    if "OCEAN CITY KIOSK" in content:
                        print(f"   ✔ Business name found")
                    else:
                        print(f"   ❌ Business name not found")
                        
                    if "Order Number:" in content:
                        print(f"   ✔ Order number label found")
                    else:
                        print(f"   ❌ Order number label not found")
                        
                    if "OCH-" in content:
                        print(f"   ✔ Order number format found")
                    else:
                        print(f"   ❌ Order number format not found")
                        
                    if "PAYMENT REQUIRED" in content:
                        print(f"   ✔ Payment required found")
                    else:
                        print(f"   ❌ Payment required not found")
                        
                    # Show a snippet
                    print(f"   📄 First 200 chars: {content[:200]}...")
                    
                    return True  # Found a working receipt
                    
                elif response.status_code == 302:
                    print(f"   🔄 Redirected (likely age verification)")
                elif response.status_code == 404:
                    print(f"   ❌ Order not found")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏰ Timeout for order {order_id}")
            except Exception as e:
                print(f"   ❌ Error for order {order_id}: {e}")
                
        print(f"\n❌ No working receipts found")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_receipt_simple()
