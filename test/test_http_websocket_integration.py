#!/usr/bin/env python3
"""
Test HTTP Endpoint with WebSocket Monitoring
"""
import asyncio
import websockets
import json
import requests
import time

async def test_http_endpoint_with_websocket():
    """Test actual HTTP endpoint with WebSocket monitoring"""
    print("🌐 Testing HTTP Endpoint + WebSocket Integration")
    print("=" * 60)
    
    try:
        # Step 1: Connect to WebSocket first
        uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected")
            
            # Step 2: Setup WebSocket listener
            async def listen_for_notification():
                try:
                    while True:
                        message = await asyncio.wait_for(websocket.recv(), timeout=15)
                        data = json.loads(message)
                        print(f"🔔 WebSocket notification received!")
                        print(f"   Type: {data.get('type')}")
                        print(f"   Call ID: {data.get('call', {}).get('call_id')}")
                        print(f"   Reason: {data.get('call', {}).get('reason_display')}")
                        print(f"   Priority: {data.get('call', {}).get('priority_display')}")
                        return data
                except asyncio.TimeoutError:
                    print("⏰ No WebSocket notification received within 15 seconds")
                    return None
            
            # Start listener
            listener_task = asyncio.create_task(listen_for_notification())
            
            # Step 3: Wait for WebSocket to stabilize
            await asyncio.sleep(2)
            
            # Step 4: Make HTTP request to actual endpoint without age verification
            print("📞 Making HTTP request to call-budtender endpoint...")
            
            # Make direct call to endpoint with JSON data
            call_data = {
                'reason': 'emergency',
                'priority': 'urgent',  # This will be ignored and calculated from reason
                'kiosk_id': 'HTTP_TEST_KIOSK',
                'session_id': 'test_session_123',
                'message': 'Testing HTTP endpoint with WebSocket monitoring'
            }
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/call-budtender/",
                    json=call_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                print(f"📤 HTTP Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Call created successfully!")
                    print(f"   Call ID: {result.get('call_id')}")
                    print(f"   Message: {result.get('message')}")
                    
                    # Wait for WebSocket notification
                    print("👂 Waiting for WebSocket notification...")
                    notification = await listener_task
                    
                    if notification:
                        print("🎉 SUCCESS: Complete HTTP->WebSocket flow working!")
                        return True
                    else:
                        print("⚠️  HTTP call worked, but no WebSocket notification received")
                        return False
                        
                elif response.status_code == 403:
                    response_data = response.json()
                    print(f"🔒 Age verification required: {response_data.get('error')}")
                    print("💡 This is expected - the endpoint is protected")
                    
                    # Cancel the listener since we won't get a notification
                    listener_task.cancel()
                    return False
                    
                else:
                    print(f"❌ HTTP request failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    listener_task.cancel()
                    return False
                    
            except Exception as e:
                print(f"❌ HTTP request error: {e}")
                listener_task.cancel()
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_age_verified_session():
    """Test with age verified session"""
    print("\n🔓 Testing with Age Verified Session")
    print("=" * 60)
    
    try:
        # Create a session and verify age first
        session = requests.Session()
        
        # Get the age verification page to get CSRF token
        print("📄 Getting age verification page...")
        age_page = session.get("http://127.0.0.1:8000/verify-age/")
        
        if age_page.status_code != 200:
            print(f"❌ Cannot access age verification page: {age_page.status_code}")
            return False
        
        # Extract CSRF token
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name == 'csrftoken':
                csrf_token = cookie.value
                break
        
        if not csrf_token:
            print("❌ No CSRF token found")
            return False
        
        print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
        
        # Submit age verification
        print("✅ Submitting age verification...")
        age_data = {
            'is_21_plus': 'on',
            'csrfmiddlewaretoken': csrf_token
        }
        
        verify_response = session.post(
            "http://127.0.0.1:8000/verify-age/",
            data=age_data,
            headers={'Referer': 'http://127.0.0.1:8000/verify-age/'}
        )
        
        print(f"📤 Age verification response: {verify_response.status_code}")
        
        if verify_response.status_code in [200, 302]:  # Success or redirect
            print("✅ Age verification successful")
            
            # Now test WebSocket with verified session
            return await test_with_verified_session(session, csrf_token)
        else:
            print(f"❌ Age verification failed: {verify_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Age verification test failed: {e}")
        return False

async def test_with_verified_session(session, csrf_token):
    """Test call with age verified session"""
    print("📞 Testing call with verified session...")
    
    try:
        # Connect to WebSocket
        uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected for verified session test")
            
            # Setup listener
            async def listen_for_notification():
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(message)
                    print(f"🔔 Verified session notification: {data.get('type')}")
                    return data
                except asyncio.TimeoutError:
                    print("⏰ No notification from verified session")
                    return None
            
            listener_task = asyncio.create_task(listen_for_notification())
            await asyncio.sleep(1)
            
            # Make call with verified session
            call_data = {
                'reason': 'product_help',
                'kiosk_id': 'VERIFIED_SESSION_TEST',
                'message': 'Testing with age verified session'
            }
            
            response = session.post(
                "http://127.0.0.1:8000/call-budtender/",
                json=call_data,
                headers={
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                }
            )
            
            print(f"📤 Verified call response: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Verified call created: {result.get('call_id')}")
                
                notification = await listener_task
                return notification is not None
            else:
                print(f"❌ Verified call failed: {response.text}")
                listener_task.cancel()
                return False
                
    except Exception as e:
        print(f"❌ Verified session test failed: {e}")
        return False

async def main():
    """Run comprehensive HTTP + WebSocket tests"""
    print("🚀 HTTP ENDPOINT + WEBSOCKET INTEGRATION TEST")
    print("=" * 70)
    
    # Test 1: Basic HTTP endpoint (will fail due to age verification)
    print("📊 Test 1: Basic HTTP Endpoint (Age Protection Expected)")
    basic_success = await test_http_endpoint_with_websocket()
    
    # Test 2: Age verified session
    print("\n📊 Test 2: Age Verified Session Integration")
    verified_success = await test_age_verified_session()
    
    # Final report
    print("\n" + "=" * 70)
    print("📋 HTTP + WEBSOCKET TEST RESULTS")
    print("=" * 70)
    
    print(f"🔒 Basic HTTP Test: {'✅ PASS' if basic_success else '❌ FAIL (Expected - Age Protection)'}")
    print(f"🔓 Verified Session Test: {'✅ PASS' if verified_success else '❌ FAIL'}")
    
    if verified_success:
        print("\n🎉 COMPLETE SUCCESS!")
        print("   🚀 HTTP->WebSocket integration is working!")
        print("   🔧 The enhanced budtender call system is operational")
        return True
    else:
        print("\n⚠️  WebSocket integration needs attention")
        print("   Check the threading approach in views.py")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
