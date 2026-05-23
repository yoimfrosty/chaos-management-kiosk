#!/usr/bin/env python3
"""
Direct Database + WebSocket Test
Creates call in database and manually triggers WebSocket broadcast
"""
import asyncio
import websockets
import json
import sys
import os
import django

# Setup Django
sys.path.append('/Users/uba/Desktop/hemp-app/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import BudtenderCall
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from datetime import datetime

class DirectWebSocketTest:
    def __init__(self):
        self.notifications_received = []
        
    async def test_websocket_with_database_call(self):
        """Test WebSocket by creating call in database and manually broadcasting"""
        print("🔗 Direct Database + WebSocket Test")
        print("=" * 60)
        
        try:
            # Connect to WebSocket first
            uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
            async with websockets.connect(uri) as websocket:
                print("✅ WebSocket connected")
                
                # Setup notification listener
                async def listen_for_notification():
                    try:
                        while True:
                            message = await asyncio.wait_for(websocket.recv(), timeout=8)
                            data = json.loads(message)
                            self.notifications_received.append(data)
                            print(f"🔔 Received notification: {data.get('type')} - {data.get('call', {}).get('reason_display')}")
                            return data
                    except asyncio.TimeoutError:
                        print("⏰ No notification received within 8 seconds")
                        return None
                
                # Start listener
                listener_task = asyncio.create_task(listen_for_notification())
                
                # Wait for connection to stabilize
                await asyncio.sleep(1)
                
                # Create call directly in database
                print("📞 Creating call directly in database...")
                call = await sync_to_async(BudtenderCall.objects.create)(
                    kiosk_id='DIRECT_TEST_KIOSK',
                    reason='product_help',
                    priority='high',
                    customer_message='Direct database test for WebSocket notifications'
                )
                
                print(f"✅ Call created in database: {call.call_id}")
                
                # Manually trigger WebSocket broadcast (like the view does)
                print("📡 Manually broadcasting WebSocket notification...")
                
                channel_layer = get_channel_layer()
                
                call_data = {
                    'call_id': str(call.call_id),
                    'kiosk_id': call.kiosk_id,
                    'reason': call.reason,
                    'reason_display': call.get_reason_display(),
                    'priority': call.priority,
                    'priority_display': call.get_priority_display(),
                    'status': call.status,
                    'customer_message': call.customer_message,
                    'created_at': call.created_at.isoformat(),
                    'session_id': call.session_id,
                }
                
                # Send to WebSocket group (same as view does)
                await channel_layer.group_send(
                    'budtender_calls',
                    {
                        'type': 'budtender_call_notification',
                        'call': call_data,
                        'message_type': 'budtender_call'
                    }
                )
                
                print("📤 WebSocket broadcast sent")
                
                # Wait for notification
                print("👂 Waiting for WebSocket notification...")
                notification = await listener_task
                
                if notification:
                    print("🎉 SUCCESS: WebSocket notification received!")
                    print(f"   Call ID: {notification.get('call', {}).get('call_id')}")
                    print(f"   Reason: {notification.get('call', {}).get('reason_display')}")
                    print(f"   Priority: {notification.get('call', {}).get('priority_display')}")
                    return True
                else:
                    print("❌ FAILED: No WebSocket notification received")
                    return False
                    
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_multiple_websocket_endpoints(self):
        """Test all WebSocket endpoints for notifications"""
        print("\n🔌 Testing Multiple WebSocket Endpoints")
        print("=" * 60)
        
        endpoints = [
            ("Admin Interface", "ws://127.0.0.1:8000/ws/budtender-calls/"),
            ("Budtender Dashboard", "ws://127.0.0.1:8000/ws/budtender/"),
            ("Legacy Notifications", "ws://127.0.0.1:8000/ws/budtender-notifications/")
        ]
        
        websockets_connected = []
        
        try:
            # Connect to all endpoints
            for name, uri in endpoints:
                try:
                    ws = await websockets.connect(uri)
                    websockets_connected.append((name, ws))
                    print(f"✅ {name}: Connected")
                except Exception as e:
                    print(f"❌ {name}: Failed - {e}")
            
            if not websockets_connected:
                print("❌ No WebSocket connections established")
                return False
            
            # Create listeners for all connected WebSockets
            async def listen_to_websocket(name, ws):
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=6)
                    data = json.loads(message)
                    print(f"🔔 {name} received: {data.get('type')}")
                    return data
                except asyncio.TimeoutError:
                    print(f"⏰ {name}: No notification within 6 seconds")
                    return None
                except Exception as e:
                    print(f"❌ {name} error: {e}")
                    return None
            
            # Start listeners for all WebSockets
            listener_tasks = []
            for name, ws in websockets_connected:
                task = asyncio.create_task(listen_to_websocket(name, ws))
                listener_tasks.append(task)
            
            # Wait for connections to stabilize
            await asyncio.sleep(1)
            
            # Create and broadcast a test notification
            print("📡 Broadcasting test notification to all endpoints...")
            
            call = await sync_to_async(BudtenderCall.objects.create)(
                kiosk_id='MULTI_ENDPOINT_TEST',
                reason='emergency',
                priority='urgent',
                customer_message='Testing multiple WebSocket endpoints'
            )
            
            channel_layer = get_channel_layer()
            call_data = {
                'call_id': str(call.call_id),
                'kiosk_id': call.kiosk_id,
                'reason': call.reason,
                'reason_display': call.get_reason_display(),
                'priority': call.priority,
                'priority_display': call.get_priority_display(),
                'status': call.status,
                'customer_message': call.customer_message,
                'created_at': call.created_at.isoformat(),
            }
            
            await channel_layer.group_send(
                'budtender_calls',
                {
                    'type': 'budtender_call_notification',
                    'call': call_data,
                    'message_type': 'budtender_call'
                }
            )
            
            print("📤 Broadcast sent, waiting for responses...")
            
            # Wait for all listeners
            results = await asyncio.gather(*listener_tasks, return_exceptions=True)
            
            # Analyze results
            success_count = 0
            for i, (name, _) in enumerate(websockets_connected):
                if i < len(results) and results[i] and not isinstance(results[i], Exception):
                    success_count += 1
            
            print(f"📊 Results: {success_count}/{len(websockets_connected)} endpoints received notifications")
            
            # Close all WebSockets
            for name, ws in websockets_connected:
                await ws.close()
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Multi-endpoint test failed: {e}")
            # Close any open WebSockets
            for name, ws in websockets_connected:
                try:
                    await ws.close()
                except:
                    pass
            return False

async def main():
    """Run comprehensive WebSocket tests"""
    print("🚀 COMPREHENSIVE WEBSOCKET SYSTEM TEST")
    print("=" * 70)
    
    tester = DirectWebSocketTest()
    
    try:
        # Test 1: Direct database + WebSocket
        print("📊 Test 1: Direct Database + WebSocket Broadcasting")
        direct_success = await tester.test_websocket_with_database_call()
        
        # Test 2: Multiple endpoint testing
        print("\n📊 Test 2: Multiple WebSocket Endpoint Testing")
        multi_success = await tester.test_multiple_websocket_endpoints()
        
        # Final report
        print("\n" + "=" * 70)
        print("📋 FINAL WEBSOCKET TEST REPORT")
        print("=" * 70)
        
        print(f"🔗 Direct WebSocket Test: {'✅ PASS' if direct_success else '❌ FAIL'}")
        print(f"🔌 Multi-Endpoint Test: {'✅ PASS' if multi_success else '❌ FAIL'}")
        print(f"📥 Notifications Received: {len(tester.notifications_received)}")
        
        if direct_success and multi_success:
            print("\n🎉 COMPLETE SUCCESS!")
            print("   ✨ WebSocket notification system is fully operational")
            print("   🚀 Enhanced budtender call system ready for production")
            print("\n🎯 Next Steps:")
            print("   1. Test frontend modal at: http://127.0.0.1:8000")
            print("   2. Access admin interface: http://127.0.0.1:8000/admin/")
            print("   3. Monitor real-time call notifications")
            return True
        elif direct_success or multi_success:
            print("\n⚠️  PARTIAL SUCCESS")
            print("   Some WebSocket functionality is working")
            print("   Check individual component failures above")
            return False
        else:
            print("\n❌ WEBSOCKET SYSTEM FAILURE")
            print("   WebSocket notifications are not working")
            print("   Check server configuration and channel layer setup")
            return False
            
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
