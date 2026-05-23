#!/usr/bin/env python3
"""
Direct WebSocket Notification Test
Tests the exact WebSocket broadcast functionality
"""
import asyncio
import websockets
import json
import requests
import time
from datetime import datetime

async def test_direct_websocket_notification():
    """Test WebSocket notification directly with a real call"""
    print("🔗 Direct WebSocket Notification Test")
    print("=" * 50)
    
    # Connect to WebSocket first
    try:
        uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully")
            
            # Create a notification listener task
            async def listen_for_notification():
                try:
                    while True:
                        message = await asyncio.wait_for(websocket.recv(), timeout=10)
                        data = json.loads(message)
                        print(f"🔔 Received: {data}")
                        return data
                except asyncio.TimeoutError:
                    print("⏰ No notification received within 10 seconds")
                    return None
            
            # Start listener
            listener_task = asyncio.create_task(listen_for_notification())
            
            # Wait a moment for connection to stabilize
            await asyncio.sleep(1)
            
            # Make HTTP request to create call (this should trigger WebSocket)
            print("📞 Making HTTP request to create budtender call...")
            
            try:
                # Get CSRF token first
                response = requests.get("http://127.0.0.1:8000/")
                if response.status_code == 200:
                    # Extract CSRF token from cookies
                    csrf_token = None
                    for cookie in response.cookies:
                        if cookie.name == 'csrftoken':
                            csrf_token = cookie.value
                            break
                    
                    if not csrf_token:
                        print("⚠️  No CSRF token found, trying without it...")
                    
                    # Make the call request
                    call_data = {
                        'reason': 'product_help',
                        'kiosk_id': 'WEBSOCKET_TEST',
                        'message': 'Testing WebSocket notification broadcast'
                    }
                    
                    headers = {
                        'Content-Type': 'application/json',
                    }
                    
                    if csrf_token:
                        headers['X-CSRFToken'] = csrf_token
                    
                    call_response = requests.post(
                        "http://127.0.0.1:8000/call-budtender/",
                        json=call_data,
                        headers=headers,
                        cookies=response.cookies,
                        timeout=5
                    )
                    
                    print(f"📤 Call request status: {call_response.status_code}")
                    if call_response.status_code == 200:
                        result = call_response.json()
                        print(f"✅ Call created: {result.get('call_id')}")
                    else:
                        print(f"❌ Call failed: {call_response.text}")
                        
                else:
                    print(f"❌ Failed to get CSRF token: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ HTTP request failed: {e}")
            
            # Wait for notification
            print("👂 Waiting for WebSocket notification...")
            notification = await listener_task
            
            if notification:
                print("🎉 WebSocket notification test PASSED!")
                return True
            else:
                print("❌ WebSocket notification test FAILED!")
                return False
                
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

async def test_manual_websocket_send():
    """Test manual WebSocket message sending"""
    print("\n🧪 Manual WebSocket Send Test")
    print("=" * 50)
    
    try:
        uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected")
            
            # Send a manual test message to the WebSocket
            test_message = {
                "type": "test_message",
                "message": "Hello from manual test",
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(test_message))
            print(f"📤 Sent manual message: {test_message}")
            
            # Try to receive any response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3)
                print(f"📥 Received response: {response}")
                return True
            except asyncio.TimeoutError:
                print("⏰ No response to manual message (this is expected)")
                return True  # This is actually expected behavior
                
    except Exception as e:
        print(f"❌ Manual WebSocket test failed: {e}")
        return False

async def main():
    """Run all WebSocket tests"""
    print("🚀 WebSocket Notification System Tests")
    print("=" * 60)
    
    # Test 1: Manual WebSocket communication
    manual_success = await test_manual_websocket_send()
    
    # Test 2: Direct notification via HTTP call
    notification_success = await test_direct_websocket_notification()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Manual WebSocket: {'✅ PASS' if manual_success else '❌ FAIL'}")
    print(f"   HTTP->WebSocket: {'✅ PASS' if notification_success else '❌ FAIL'}")
    
    if manual_success and notification_success:
        print("\n🎉 All WebSocket tests PASSED!")
        print("   WebSocket system is fully functional")
    elif manual_success:
        print("\n⚠️  WebSocket connection works, but HTTP->WebSocket notifications need debugging")
        print("   Check Django view WebSocket broadcast code")
    else:
        print("\n❌ WebSocket system needs attention")
        print("   Check server configuration and WebSocket routing")

if __name__ == "__main__":
    asyncio.run(main())
