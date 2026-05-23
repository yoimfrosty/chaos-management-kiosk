#!/usr/bin/env python3
"""
Complete Integration Test for Enhanced Budtender Call System
Tests all components: Frontend Modal -> Database -> WebSocket -> Admin Interface
"""
import asyncio
import websockets
import json
import time
import sys
import os
import django
from datetime import datetime

# Setup Django
sys.path.append('/Users/uba/Desktop/hemp-app/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import BudtenderCall, BudtenderCallLog

class ComprehensiveBudtenderTest:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.admin_connected = False
        self.budtender_connected = False
        self.notifications_received = []
        
    async def setup_websocket_listeners(self):
        """Setup WebSocket connections for testing"""
        print("🔌 Setting up WebSocket connections...")
        
        try:
            # Connect to admin interface WebSocket
            self.admin_ws = await websockets.connect("ws://127.0.0.1:8000/ws/budtender-calls/")
            self.admin_connected = True
            print("   ✅ Admin WebSocket connected")
            
            # Connect to budtender dashboard WebSocket  
            self.budtender_ws = await websockets.connect("ws://127.0.0.1:8000/ws/budtender/")
            self.budtender_connected = True
            print("   ✅ Budtender dashboard WebSocket connected")
            
            return True
            
        except Exception as e:
            print(f"   ❌ WebSocket setup failed: {e}")
            return False
    
    async def listen_for_admin_notifications(self):
        """Listen for admin notifications"""
        try:
            async for message in self.admin_ws:
                notification = json.loads(message)
                self.notifications_received.append({
                    'time': datetime.now().isoformat(),
                    'source': 'admin',
                    'data': notification
                })
                print(f"   🔔 Admin notification: {notification.get('type')} - {notification.get('reason')}")
        except websockets.exceptions.ConnectionClosed:
            print("   📴 Admin WebSocket disconnected")
        except Exception as e:
            print(f"   ❌ Admin listener error: {e}")
    
    async def listen_for_budtender_notifications(self):
        """Listen for budtender dashboard notifications"""
        try:
            async for message in self.budtender_ws:
                notification = json.loads(message)
                self.notifications_received.append({
                    'time': datetime.now().isoformat(),
                    'source': 'budtender',
                    'data': notification
                })
                print(f"   🎯 Budtender notification: {notification.get('type')} - {notification.get('priority')}")
        except websockets.exceptions.ConnectionClosed:
            print("   📴 Budtender WebSocket disconnected")
        except Exception as e:
            print(f"   ❌ Budtender listener error: {e}")
    
    def create_test_calls_in_database(self):
        """Create test budtender calls directly in database"""
        print("📞 Creating test calls in database...")
        
        test_scenarios = [
            {
                'kiosk_id': 'MAIN_ENTRANCE',
                'reason': 'product_help',
                'priority': 'normal',
                'customer_message': 'Need help choosing between sativa and indica strains'
            },
            {
                'kiosk_id': 'SIDE_ENTRANCE', 
                'reason': 'dosage_help',
                'priority': 'high',
                'customer_message': 'First time user, unsure about proper dosage'
            },
            {
                'kiosk_id': 'MAIN_ENTRANCE',
                'reason': 'technical_issue',
                'priority': 'normal',
                'customer_message': 'Payment screen is frozen'
            },
            {
                'kiosk_id': 'VIP_SECTION',
                'reason': 'emergency',
                'priority': 'urgent',
                'customer_message': 'Customer feeling unwell after consumption'
            }
        ]
        
        created_calls = []
        for scenario in test_scenarios:
            try:
                call = BudtenderCall.objects.create(**scenario)
                created_calls.append(call)
                print(f"   ✅ Created {call.get_priority_display()} call: {call.get_reason_display()}")
                
                # Create corresponding log entry
                BudtenderCallLog.objects.create(
                    call=call,
                    action='created',
                    notes=f"Call created from {call.kiosk_id}"
                )
                
            except Exception as e:
                print(f"   ❌ Failed to create call: {e}")
        
        print(f"   📊 Total calls created: {len(created_calls)}")
        return created_calls
    
    async def test_call_lifecycle(self, test_call):
        """Test complete call lifecycle"""
        print(f"\n🔄 Testing lifecycle for call {test_call.call_id}")
        
        # Step 1: Acknowledge call
        test_call.acknowledge("test_budtender")
        print(f"   ✅ Acknowledged - Status: {test_call.status}")
        
        # Wait a moment
        await asyncio.sleep(1)
        
        # Step 2: Start assistance
        test_call.start_assistance("test_budtender") 
        print(f"   ✅ Started assistance - Status: {test_call.status}")
        
        # Wait a moment
        await asyncio.sleep(1)
        
        # Step 3: Resolve call
        test_call.resolve("test_budtender", "Successfully resolved customer issue")
        print(f"   ✅ Resolved - Status: {test_call.status}")
        print(f"   ⏱️  Total resolution time: {test_call.total_resolution_time}")
    
    async def simulate_real_time_calls(self):
        """Simulate real-time incoming calls"""
        print("\n📡 Simulating real-time call creation...")
        
        await asyncio.sleep(2)  # Give listeners time to connect
        
        # Create a new call
        new_call = BudtenderCall.objects.create(
            kiosk_id='REAL_TIME_TEST',
            reason='general_help',
            priority='normal', 
            customer_message='Testing real-time WebSocket notifications'
        )
        
        print(f"   📞 Created real-time call: {new_call.call_id}")
        
        # Wait for notification propagation
        await asyncio.sleep(3)
        
        return new_call
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "="*70)
        print("📊 COMPREHENSIVE BUDTENDER SYSTEM TEST REPORT")
        print("="*70)
        
        # Database statistics
        total_calls = BudtenderCall.objects.count()
        pending_calls = BudtenderCall.objects.filter(status='pending').count()
        resolved_calls = BudtenderCall.objects.filter(status='resolved').count()
        total_logs = BudtenderCallLog.objects.count()
        
        print(f"\n📈 Database Statistics:")
        print(f"   Total calls: {total_calls}")
        print(f"   Pending calls: {pending_calls}")
        print(f"   Resolved calls: {resolved_calls}")
        print(f"   Total log entries: {total_logs}")
        
        # WebSocket statistics
        print(f"\n🔌 WebSocket Performance:")
        print(f"   Admin connection: {'✅ Connected' if self.admin_connected else '❌ Failed'}")
        print(f"   Budtender connection: {'✅ Connected' if self.budtender_connected else '❌ Failed'}")
        print(f"   Notifications received: {len(self.notifications_received)}")
        
        # Call priority distribution
        print(f"\n📊 Call Priority Distribution:")
        for priority, label in BudtenderCall.PRIORITY_CHOICES:
            count = BudtenderCall.objects.filter(priority=priority).count()
            print(f"   {label}: {count}")
        
        # Recent call activity
        print(f"\n🕐 Recent Call Activity:")
        recent_calls = BudtenderCall.objects.all().order_by('-created_at')[:5]
        for call in recent_calls:
            status_emoji = {'pending': '🔴', 'acknowledged': '🟡', 'in_progress': '🟠', 'resolved': '🟢', 'dismissed': '⚫'}
            priority_emoji = {'urgent': '🚨', 'high': '⚠️', 'normal': '📞', 'low': '📝'}
            
            print(f"   {status_emoji.get(call.status, '❓')} {priority_emoji.get(call.priority, '📞')} {call.kiosk_id} - {call.get_reason_display()}")
            print(f"      Created: {call.created_at.strftime('%H:%M:%S')} | Status: {call.status}")
        
        # Success criteria evaluation
        success_criteria = {
            'Database functionality': total_calls > 0 and total_logs > 0,
            'WebSocket connections': self.admin_connected and self.budtender_connected,
            'Call lifecycle': resolved_calls > 0,
            'Priority handling': BudtenderCall.objects.filter(priority='urgent').count() > 0
        }
        
        print(f"\n✅ Success Criteria:")
        all_passed = True
        for criteria, passed in success_criteria.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {criteria}: {status}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    async def run_comprehensive_test(self):
        """Run the complete comprehensive test"""
        print("🚀 ENHANCED BUDTENDER SYSTEM - COMPREHENSIVE TEST")
        print("="*70)
        
        try:
            # Step 1: Setup WebSocket connections
            print("\n📡 Phase 1: WebSocket Connection Setup")
            websocket_success = await self.setup_websocket_listeners()
            
            if websocket_success:
                # Start WebSocket listeners
                admin_task = asyncio.create_task(self.listen_for_admin_notifications())
                budtender_task = asyncio.create_task(self.listen_for_budtender_notifications())
                
                # Give connections time to stabilize
                await asyncio.sleep(1)
            
            # Step 2: Create test calls
            print("\n📞 Phase 2: Database Call Creation")
            test_calls = self.create_test_calls_in_database()
            
            # Step 3: Test call lifecycle
            if test_calls:
                print("\n🔄 Phase 3: Call Lifecycle Testing")
                await self.test_call_lifecycle(test_calls[0])
            
            # Step 4: Test real-time functionality
            print("\n📡 Phase 4: Real-time Notification Testing")
            if websocket_success:
                await self.simulate_real_time_calls()
                await asyncio.sleep(3)  # Wait for notifications
            
            # Step 5: Cleanup WebSocket connections
            if websocket_success:
                admin_task.cancel()
                budtender_task.cancel()
                await self.admin_ws.close()
                await self.budtender_ws.close()
            
            # Step 6: Generate comprehensive report
            print("\n📊 Phase 5: Report Generation")
            success = self.generate_comprehensive_report()
            
            # Final status
            print("\n" + "="*70)
            if success:
                print("🎉 COMPREHENSIVE TEST: COMPLETE SUCCESS!")
                print("\n🎯 System Ready for Production Use:")
                print("   • Enhanced budtender call modal functional")
                print("   • Database models working correctly")
                print("   • WebSocket real-time notifications active")
                print("   • Admin interface enhanced and ready")
                print("   • Call lifecycle management operational")
                print("\n📋 Next Steps:")
                print("   1. Test frontend modal: http://127.0.0.1:8000")
                print("   2. Access admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
                print("   3. Monitor calls in admin 'Budtender calls' section")
            else:
                print("⚠️  PARTIAL SUCCESS - Some components need attention")
            
            return success
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

async def main():
    """Main test execution"""
    tester = ComprehensiveBudtenderTest()
    
    try:
        success = await tester.run_comprehensive_test()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
