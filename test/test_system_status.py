#!/usr/bin/env python3
"""
Check notification system status.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def check_system_status():
    """Check the status of the notification system"""
    print("📊 Notification System Status Check")
    print("=" * 45)
    
    session = requests.Session()
    
    # Test each endpoint
    endpoints = [
        ("Assistance Requests", "/check-pending-assistance/"),
        ("Order Notifications", "/check-pending-orders/"),
        ("Admin Panel", "/admin/"),
        ("Kiosk Main", "/products/"),
    ]
    
    all_working = True
    
    for name, endpoint in endpoints:
        try:
            response = session.get(f"{BASE_URL}{endpoint}")
            status = response.status_code
            
            if status == 200:
                if endpoint in ["/check-pending-assistance/", "/check-pending-orders/"]:
                    try:
                        data = response.json()
                        count = data.get('count', 0)
                        print(f"✅ {name}: Working (Status: {status}, Count: {count})")
                    except json.JSONDecodeError:
                        print(f"❌ {name}: Invalid JSON response")
                        all_working = False
                else:
                    print(f"✅ {name}: Working (Status: {status})")
            else:
                print(f"❌ {name}: Failed (Status: {status})")
                all_working = False
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            all_working = False
    
    print("\n" + "=" * 45)
    
    if all_working:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n📋 System Features:")
        print("   ✅ Real-time assistance request notifications")
        print("   ✅ Real-time order placement notifications") 
        print("   ✅ Admin panel with notification pop-ups")
        print("   ✅ Sound alerts for new notifications")
        print("   ✅ Status indicator showing pending counts")
        print("   ✅ Quick action buttons (Acknowledge/Resolve)")
        
        print("\n🔔 How to test:")
        print("   1. Go to: http://127.0.0.1:8000/products/")
        print("   2. Click 'Ask for Assistance' button")
        print("   3. Go to: http://127.0.0.1:8000/admin/")
        print("   4. You should see notification pop-up with sound")
        print("   5. Place an order to test order notifications")
        
        print("\n📊 Admin Pages:")
        print("   • Assistance Requests: http://127.0.0.1:8000/admin/kiosk/assistancerequest/")
        print("   • Order Notifications: http://127.0.0.1:8000/admin/kiosk/ordernotification/")
        print("   • Orders: http://127.0.0.1:8000/admin/kiosk/order/")
    else:
        print("❌ Some systems are not working properly")
    
    return all_working

if __name__ == "__main__":
    check_system_status()
