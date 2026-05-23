#!/usr/bin/env python3
"""
Network Connectivity Test for Hemp App
Test the app from another device on the same network
"""

import requests
import socket
import sys
from datetime import datetime

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Unable to determine"

def test_server_accessibility():
    """Test if the Django server is accessible"""
    local_ip = get_local_ip()
    test_urls = [
        f"http://{local_ip}:8000/",
        "http://localhost:8000/",
        "http://127.0.0.1:8000/"
    ]
    
    print("🧪 Testing Django Server Accessibility")
    print("=" * 50)
    print(f"📍 Local IP Address: {local_ip}")
    print(f"🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url} - ACCESSIBLE (Status: {response.status_code})")
            else:
                print(f"⚠️  {url} - ACCESSIBLE but status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - CONNECTION REFUSED")
        except requests.exceptions.Timeout:
            print(f"⏰ {url} - TIMEOUT")
        except Exception as e:
            print(f"❌ {url} - ERROR: {str(e)}")
    
    print()
    print("📱 Instructions for Testing from Another Device:")
    print("=" * 50)
    print(f"1. Connect your test device to the same WiFi network")
    print(f"2. Open a web browser on the test device")
    print(f"3. Navigate to: http://{local_ip}:8000/")
    print(f"4. You should see the Hemp Kiosk interface")
    print(f"5. Test the 'Call Budtender' feature for audio notifications")
    print()
    print("🔧 Admin Panel Access:")
    print(f"   http://{local_ip}:8000/admin/")
    print()
    print("🎵 Features to Test:")
    print("   • Age verification")
    print("   • Product browsing")
    print("   • Cart functionality")
    print("   • Budtender notifications (AUDIO)")
    print("   • Checkout process")

def test_port_availability():
    """Test if port 8000 is available/in use"""
    print("🔌 Testing Port Availability")
    print("=" * 30)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex(('localhost', 8000))
        if result == 0:
            print("✅ Port 8000 is in use (Django server running)")
        else:
            print("❌ Port 8000 is not in use (Django server not running)")
    except Exception as e:
        print(f"❌ Error testing port: {e}")
    finally:
        sock.close()
    print()

if __name__ == "__main__":
    print("🌿 Hemp App Network Connectivity Test")
    print("=" * 60)
    print()
    
    test_port_availability()
    test_server_accessibility()
    
    print("💡 Troubleshooting Tips:")
    print("=" * 25)
    print("• If connection fails, check your firewall settings")
    print("• Ensure both devices are on the same WiFi network")
    print("• Try disabling macOS firewall temporarily for testing")
    print("• Verify the Django server is running with:")
    print("  python3 manage.py runserver 0.0.0.0:8000")
