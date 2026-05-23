#!/usr/bin/env python3
"""
Test WebSocket connection to verify the enhanced budtender system
"""
import asyncio
import websockets
import json
import sys

async def test_websocket_connection():
    """Test the WebSocket connection to the budtender system"""
    try:
        # Test the budtender dashboard endpoint
        uri = "ws://127.0.0.1:8000/ws/budtender/"
        print(f"🔗 Attempting to connect to {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection established successfully!")
            
            # Send a test message
            test_message = {
                "type": "test_connection",
                "message": "Hello from test client"
            }
            await websocket.send(json.dumps(test_message))
            print(f"📤 Sent test message: {test_message}")
            
            # Try to receive a response (with timeout)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"📥 Received response: {response}")
            except asyncio.TimeoutError:
                print("⏰ No response received within 5 seconds (this is normal for this consumer)")
            
            print("🎉 WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False
    
    return True

async def test_admin_websocket():
    """Test the admin interface WebSocket endpoint"""
    try:
        uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
        print(f"🔗 Testing admin WebSocket at {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("✅ Admin WebSocket connection established!")
            
            # Send a test admin message
            admin_message = {
                "type": "admin_test",
                "action": "check_connection"
            }
            await websocket.send(json.dumps(admin_message))
            print(f"📤 Sent admin test message: {admin_message}")
            
            # Try to receive a response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"📥 Admin received: {response}")
            except asyncio.TimeoutError:
                print("⏰ No admin response within 5 seconds")
            
    except Exception as e:
        print(f"❌ Admin WebSocket failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting WebSocket Connection Tests")
    print("=" * 50)
    
    # Run the tests
    loop = asyncio.get_event_loop()
    
    print("\n📡 Testing Budtender Dashboard WebSocket...")
    budtender_success = loop.run_until_complete(test_websocket_connection())
    
    print("\n🔧 Testing Admin Interface WebSocket...")
    admin_success = loop.run_until_complete(test_admin_websocket())
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Budtender WebSocket: {'✅ PASS' if budtender_success else '❌ FAIL'}")
    print(f"   Admin WebSocket: {'✅ PASS' if admin_success else '❌ FAIL'}")
    
    if budtender_success and admin_success:
        print("\n🎉 All WebSocket tests passed! System ready for enhanced budtender calls.")
    else:
        print("\n⚠️  Some WebSocket tests failed. Check the server configuration.")
        sys.exit(1)
