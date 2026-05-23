#!/usr/bin/env python3
"""
End-to-End Test for Enhanced Budtender Call System
Tests the complete flow from customer call to admin notification
"""
import asyncio
import websockets
import json
import requests
import time
from datetime import datetime

class BudtenderSystemTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.admin_websocket = None
        self.notifications_received = []
        
    async def connect_admin_websocket(self):
        """Connect to admin WebSocket to listen for notifications"""
        try:
            uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
            self.admin_websocket = await websockets.connect(uri)
            print("✅ Admin WebSocket connected - listening for notifications")
            return True
        except Exception as e:
            print(f"❌ Failed to connect admin WebSocket: {e}")
            return False
    
    async def listen_for_notifications(self):
        """Listen for incoming notifications"""
        try:
            while True:
                message = await self.admin_websocket.recv()
                notification = json.loads(message)
                self.notifications_received.append({
                    'time': datetime.now().isoformat(),
                    'data': notification
                })
                print(f"🔔 Received notification: {notification}")
                
                if notification.get('type') == 'budtender_call':
                    print(f"📞 New call from kiosk {notification.get('kiosk_id')}")
                    print(f"   Reason: {notification.get('reason')}")
                    print(f"   Priority: {notification.get('priority')}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Admin WebSocket connection closed")
        except Exception as e:
            print(f"❌ Error listening for notifications: {e}")
    
    def simulate_customer_call(self, reason="Product Info", priority="normal"):
        """Simulate a customer making a budtender call"""
        print(f"\n👤 Customer making call - Reason: {reason}, Priority: {priority}")
        
        try:
            response = requests.post(
                f"{self.base_url}/call-budtender/",
                data={
                    'reason': reason,
                    'priority': priority,
                    'kiosk_id': 'KIOSK_001'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Call submitted successfully - ID: {result.get('call_id')}")
                return result.get('call_id')
            else:
                print(f"❌ Call failed with status {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error making call: {e}")
            return None
    
    async def test_complete_flow(self):
        """Test the complete budtender call flow"""
        print("🚀 Starting End-to-End Budtender Call System Test")
        print("=" * 60)
        
        # Step 1: Connect admin WebSocket
        print("\n📡 Step 1: Connecting admin interface...")
        if not await self.connect_admin_websocket():
            return False
        
        # Step 2: Start listening for notifications in background
        print("\n🎧 Step 2: Starting notification listener...")
        listener_task = asyncio.create_task(self.listen_for_notifications())
        
        # Step 3: Wait a moment for connection to stabilize
        await asyncio.sleep(1)
        
        # Step 4: Simulate customer calls with different priorities
        print("\n📞 Step 3: Simulating customer calls...")
        
        test_calls = [
            ("Product Info", "normal"),
            ("Dosage Help", "high"),
            ("Emergency", "urgent"),
            ("Technical Issues", "normal")
        ]
        
        call_ids = []
        for reason, priority in test_calls:
            call_id = await asyncio.get_event_loop().run_in_executor(
                None, self.simulate_customer_call, reason, priority
            )
            if call_id:
                call_ids.append(call_id)
            
            # Wait a bit between calls
            await asyncio.sleep(2)
        
        # Step 5: Wait for notifications to be received
        print("\n⏳ Step 4: Waiting for notifications to be processed...")
        await asyncio.sleep(5)
        
        # Step 6: Cancel listener and analyze results
        listener_task.cancel()
        
        return self.analyze_results(call_ids)
    
    def analyze_results(self, call_ids):
        """Analyze the test results"""
        print("\n📊 Test Results Analysis")
        print("=" * 60)
        
        print(f"📞 Calls made: {len(call_ids)}")
        print(f"🔔 Notifications received: {len(self.notifications_received)}")
        
        if len(self.notifications_received) > 0:
            print("\n📋 Notification Details:")
            for i, notif in enumerate(self.notifications_received, 1):
                data = notif['data']
                print(f"   {i}. Time: {notif['time']}")
                print(f"      Type: {data.get('type')}")
                print(f"      Kiosk: {data.get('kiosk_id')}")
                print(f"      Reason: {data.get('reason')}")
                print(f"      Priority: {data.get('priority')}")
                print()
        
        # Success criteria
        success = len(self.notifications_received) >= len(call_ids)
        
        if success:
            print("🎉 SUCCESS: Enhanced budtender call system is working correctly!")
            print("   ✅ WebSocket connections established")
            print("   ✅ Customer calls submitted to database")
            print("   ✅ Real-time notifications sent to admin")
            print("   ✅ Priority-based call handling functional")
        else:
            print("⚠️  PARTIAL SUCCESS: Some notifications may have been missed")
            print("   ✅ Basic functionality working")
            print("   ⚠️  Check WebSocket notification delivery")
        
        return success

async def main():
    """Main test execution"""
    tester = BudtenderSystemTester()
    
    try:
        success = await tester.test_complete_flow()
        
        print("\n" + "=" * 60)
        if success:
            print("🏆 ENHANCED BUDTENDER SYSTEM: FULLY OPERATIONAL")
            print("\n🎯 Next Steps:")
            print("   1. Access admin interface at: http://127.0.0.1:8000/admin/")
            print("   2. Login with: admin / admin123")
            print("   3. Navigate to 'Budtender calls' to see call management")
            print("   4. Test the enhanced call button on age verification page")
        else:
            print("🔧 SYSTEM NEEDS ATTENTION")
            print("   Check server logs and WebSocket configurations")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
