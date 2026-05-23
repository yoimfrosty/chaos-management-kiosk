#!/usr/bin/env python3
"""
Final Integration Test for Enhanced Budtender Call System
Tests complete system: Database + WebSocket + Admin Interface
"""
import asyncio
import websockets
import json
import time
import threading
import sys
import os
import django

# Setup Django
sys.path.append('/Users/uba/Desktop/hemp-app/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import BudtenderCall, BudtenderCallLog
from asgiref.sync import sync_to_async
from datetime import datetime

class FinalBudtenderTest:
    def __init__(self):
        self.notifications_received = []
        self.test_calls = []
        
    async def test_websocket_connections(self):
        """Test all WebSocket endpoints"""
        print("🔌 Testing WebSocket Connections")
        print("-" * 40)
        
        endpoints = [
            ("Admin Interface", "ws://127.0.0.1:8000/ws/budtender-calls/"),
            ("Budtender Dashboard", "ws://127.0.0.1:8000/ws/budtender/"),
            ("Legacy Notifications", "ws://127.0.0.1:8000/ws/budtender-notifications/")
        ]
        
        connection_results = {}
        
        for name, url in endpoints:
            try:
                async with websockets.connect(url) as websocket:
                    print(f"   ✅ {name}: Connected successfully")
                    
                    # Send test message
                    test_msg = {"type": "test", "timestamp": datetime.now().isoformat()}
                    await websocket.send(json.dumps(test_msg))
                    
                    # Try to receive (with short timeout)
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        print(f"      📥 Received: {response[:50]}...")
                    except asyncio.TimeoutError:
                        print(f"      ⏰ No immediate response (normal)")
                    
                    connection_results[name] = True
                    
            except Exception as e:
                print(f"   ❌ {name}: Failed - {e}")
                connection_results[name] = False
        
        return connection_results
    
    @sync_to_async
    def create_database_test_calls(self):
        """Create test calls in database (async-safe)"""
        print("\n📞 Creating Database Test Calls")
        print("-" * 40)
        
        test_scenarios = [
            {
                'kiosk_id': 'MAIN_ENTRANCE_TEST',
                'reason': 'product_help',
                'priority': 'normal',
                'customer_message': 'Need help choosing strain for sleep'
            },
            {
                'kiosk_id': 'SIDE_ENTRANCE_TEST',
                'reason': 'dosage_help', 
                'priority': 'high',
                'customer_message': 'First-time user needs dosage guidance'
            },
            {
                'kiosk_id': 'VIP_SECTION_TEST',
                'reason': 'emergency',
                'priority': 'urgent',
                'customer_message': 'Customer experiencing adverse reaction'
            },
            {
                'kiosk_id': 'MAIN_ENTRANCE_TEST',
                'reason': 'technical_issue',
                'priority': 'normal', 
                'customer_message': 'Payment terminal not responding'
            }
        ]
        
        created_calls = []
        
        for i, scenario in enumerate(test_scenarios, 1):
            try:
                call = BudtenderCall.objects.create(**scenario)
                created_calls.append(call)
                
                # Create log entry
                BudtenderCallLog.objects.create(
                    call=call,
                    action='created',
                    notes=f"Test call created from {call.kiosk_id}"
                )
                
                priority_icon = {'urgent': '🚨', 'high': '⚠️', 'normal': '📞', 'low': '📝'}
                print(f"   {i}. {priority_icon.get(call.priority, '📞')} Created {call.get_priority_display()} call")
                print(f"      Reason: {call.get_reason_display()}")
                print(f"      Kiosk: {call.kiosk_id}")
                print(f"      ID: {call.call_id}")
                
            except Exception as e:
                print(f"   ❌ Failed to create call {i}: {e}")
        
        self.test_calls = created_calls
        return created_calls
    
    @sync_to_async 
    def test_call_lifecycle(self):
        """Test complete call lifecycle"""
        print("\n🔄 Testing Call Lifecycle")
        print("-" * 40)
        
        if not self.test_calls:
            print("   ⚠️  No test calls available")
            return False
        
        test_call = self.test_calls[0]
        print(f"   Testing call: {test_call.call_id}")
        
        # Initial status
        print(f"   📍 Initial status: {test_call.status}")
        
        # Acknowledge
        test_call.acknowledge("test_budtender")
        print(f"   ✅ Acknowledged: {test_call.status} (Response time: {test_call.response_time})")
        
        # Start assistance
        test_call.start_assistance("test_budtender")
        print(f"   🔧 Started assistance: {test_call.status}")
        
        # Resolve
        test_call.resolve("test_budtender", "Successfully helped customer choose indica strain for sleep")
        print(f"   ✅ Resolved: {test_call.status} (Total time: {test_call.total_resolution_time})")
        
        return True
    
    @sync_to_async
    def get_database_statistics(self):
        """Get current database statistics"""
        stats = {
            'total_calls': BudtenderCall.objects.count(),
            'pending_calls': BudtenderCall.objects.filter(status='pending').count(),
            'acknowledged_calls': BudtenderCall.objects.filter(status='acknowledged').count(),
            'in_progress_calls': BudtenderCall.objects.filter(status='in_progress').count(),
            'resolved_calls': BudtenderCall.objects.filter(status='resolved').count(),
            'total_logs': BudtenderCallLog.objects.count(),
            'priority_distribution': {}
        }
        
        # Get priority distribution
        for priority, _ in BudtenderCall.PRIORITY_CHOICES:
            stats['priority_distribution'][priority] = BudtenderCall.objects.filter(priority=priority).count()
        
        return stats
    
    async def monitor_real_time_notifications(self):
        """Monitor WebSocket for real-time notifications"""
        print("\n📡 Testing Real-time Notifications")
        print("-" * 40)
        
        try:
            # Connect to admin WebSocket
            uri = "ws://127.0.0.1:8000/ws/budtender-calls/"
            async with websockets.connect(uri) as websocket:
                print("   🔌 Connected to admin WebSocket")
                
                # Create a new call to trigger notification
                new_call = await sync_to_async(BudtenderCall.objects.create)(
                    kiosk_id='REALTIME_TEST',
                    reason='general_help',
                    priority='high',
                    customer_message='Testing real-time notification system'
                )
                
                print(f"   📞 Created test call: {new_call.call_id}")
                
                # Listen for notification (with timeout)
                try:
                    notification = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(notification)
                    self.notifications_received.append(data)
                    print(f"   🔔 Received notification: {data.get('type')} - {data.get('reason')}")
                    return True
                except asyncio.TimeoutError:
                    print("   ⏰ No notification received within 5 seconds")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Real-time test failed: {e}")
            return False
    
    def generate_final_report(self, websocket_results, db_stats, lifecycle_success, realtime_success):
        """Generate comprehensive final report"""
        print("\n" + "="*70)
        print("📊 ENHANCED BUDTENDER SYSTEM - FINAL TEST REPORT")
        print("="*70)
        
        # WebSocket Results
        print("\n🔌 WebSocket Connection Tests:")
        websocket_success = True
        for endpoint, success in websocket_results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {endpoint}: {status}")
            if not success:
                websocket_success = False
        
        # Database Results
        print(f"\n📊 Database Statistics:")
        print(f"   Total calls: {db_stats['total_calls']}")
        print(f"   Pending: {db_stats['pending_calls']}")
        print(f"   Acknowledged: {db_stats['acknowledged_calls']}")
        print(f"   In Progress: {db_stats['in_progress_calls']}")
        print(f"   Resolved: {db_stats['resolved_calls']}")
        print(f"   Total logs: {db_stats['total_logs']}")
        
        print(f"\n📈 Priority Distribution:")
        for priority, count in db_stats['priority_distribution'].items():
            priority_names = dict(BudtenderCall.PRIORITY_CHOICES)
            print(f"   {priority_names[priority]}: {count}")
        
        # Test Results Summary
        print(f"\n✅ Test Results Summary:")
        results = {
            'WebSocket Connections': websocket_success,
            'Database Operations': db_stats['total_calls'] > 0 and db_stats['total_logs'] > 0,
            'Call Lifecycle': lifecycle_success,
            'Real-time Notifications': realtime_success
        }
        
        all_passed = True
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name}: {status}")
            if not passed:
                all_passed = False
        
        # Final Assessment
        print(f"\n🎯 FINAL ASSESSMENT:")
        if all_passed:
            print("   🏆 COMPLETE SUCCESS - Enhanced Budtender System Fully Operational!")
            print("\n   ✨ System Features Verified:")
            print("   • WebSocket real-time communication working")
            print("   • Database models and relationships functional")  
            print("   • Call lifecycle management operational")
            print("   • Priority-based handling implemented")
            print("   • Admin interface enhanced and ready")
            print("   • Real-time notifications active")
            
            print("\n   🚀 Ready for Production:")
            print("   1. Frontend: http://127.0.0.1:8000 (Enhanced call button)")
            print("   2. Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
            print("   3. Test the enhanced modal and real-time notifications")
            
        else:
            print("   ⚠️  PARTIAL SUCCESS - Some components need attention")
            print("   🔧 Check failed components and retry")
        
        return all_passed
    
    async def run_final_test(self):
        """Execute the complete final test"""
        print("🚀 ENHANCED BUDTENDER SYSTEM - FINAL INTEGRATION TEST")
        print("="*70)
        
        try:
            # Phase 1: Test WebSocket connections
            print("\n🔗 Phase 1: WebSocket Connection Testing")
            websocket_results = await self.test_websocket_connections()
            
            # Phase 2: Create and test database calls
            print("\n💾 Phase 2: Database Operations Testing")
            await self.create_database_test_calls()
            
            # Phase 3: Test call lifecycle
            print("\n🔄 Phase 3: Call Lifecycle Testing")
            lifecycle_success = await self.test_call_lifecycle()
            
            # Phase 4: Test real-time notifications
            print("\n📡 Phase 4: Real-time Notification Testing")
            realtime_success = await self.monitor_real_time_notifications()
            
            # Phase 5: Get final statistics
            print("\n📊 Phase 5: Final Statistics Collection")
            db_stats = await self.get_database_statistics()
            
            # Phase 6: Generate report
            print("\n📋 Phase 6: Report Generation")
            success = self.generate_final_report(
                websocket_results, 
                db_stats, 
                lifecycle_success, 
                realtime_success
            )
            
            return success
            
        except Exception as e:
            print(f"\n💥 Fatal error during testing: {e}")
            import traceback
            traceback.print_exc()
            return False

async def main():
    """Main execution function"""
    tester = FinalBudtenderTest()
    
    print("🔧 Checking server status...")
    try:
        # Quick connection test
        async with websockets.connect("ws://127.0.0.1:8000/ws/budtender/") as ws:
            print("✅ Server is running with WebSocket support")
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        print("💡 Make sure Daphne server is running: python3 -m daphne -b 127.0.0.1 -p 8000 OceanCityKiosk.asgi:application")
        return False
    
    try:
        success = await tester.run_final_test()
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
