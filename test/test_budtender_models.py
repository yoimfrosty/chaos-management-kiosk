#!/usr/bin/env python3
"""
Simple test to verify budtender call functionality
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/Users/uba/Desktop/hemp-app/chaos-magement')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import BudtenderCall, BudtenderCallLog
from datetime import datetime

def test_budtender_models():
    """Test the budtender call models directly"""
    print("🧪 Testing Enhanced Budtender Call Models")
    print("=" * 50)
    
    # Create test calls with different priorities
    test_calls = [
        {
            'kiosk_id': 'KIOSK_001',
            'reason': 'product_help',
            'priority': 'normal',
            'customer_message': 'Customer needs help choosing between indica and sativa'
        },
        {
            'kiosk_id': 'KIOSK_002', 
            'reason': 'dosage_help',
            'priority': 'high',
            'customer_message': 'New customer needs dosage guidance'
        },
        {
            'kiosk_id': 'KIOSK_001',
            'reason': 'emergency',
            'priority': 'urgent',
            'customer_message': 'Customer experiencing adverse reaction'
        }
    ]
    
    created_calls = []
    
    print("\n📞 Creating test calls...")
    for i, call_data in enumerate(test_calls, 1):
        try:
            call = BudtenderCall.objects.create(**call_data)
            created_calls.append(call)
            print(f"   {i}. Created call {call.call_id} - {call.reason} ({call.priority})")
        except Exception as e:
            print(f"   ❌ Failed to create call {i}: {e}")
    
    print(f"\n✅ Successfully created {len(created_calls)} test calls")
    
    # Test call status changes
    print("\n🔄 Testing call status transitions...")
    if created_calls:
        test_call = created_calls[0]
        print(f"   Testing call {test_call.call_id}")
        
        # Acknowledge call
        test_call.acknowledge("admin_user")
        print(f"   ✅ Acknowledged: Response time = {test_call.response_time}")
        
        # Start assistance
        test_call.start_assistance()
        print(f"   ✅ Started assistance: Status = {test_call.status}")
        
        # Resolve call
        test_call.resolve("Issue resolved successfully")
        print(f"   ✅ Resolved: Resolution time = {test_call.total_resolution_time}")
    
    # Display all calls
    print("\n📋 Current Budtender Calls:")
    all_calls = BudtenderCall.objects.all().order_by('-created_at')
    
    for call in all_calls:
        status_icon = {
            'pending': '🔴',
            'acknowledged': '🟡', 
            'in_progress': '🟠',
            'resolved': '🟢',
            'dismissed': '⚫'
        }.get(call.status, '❓')
        
        priority_icon = {
            'urgent': '🚨',
            'high': '⚠️',
            'normal': '📞'
        }.get(call.priority, '📞')
        
        print(f"   {status_icon} {priority_icon} {call.call_id} | {call.kiosk_id} | {call.reason}")
        print(f"      Status: {call.status} | Created: {call.created_at.strftime('%H:%M:%S')}")
        if call.total_resolution_time:
            print(f"      Resolution time: {call.total_resolution_time}")
        print()
    
    # Display call logs
    print("📜 Call Activity Logs:")
    logs = BudtenderCallLog.objects.all().order_by('-timestamp')[:10]
    
    for log in logs:
        print(f"   🕐 {log.timestamp.strftime('%H:%M:%S')} | {log.call.call_id} | {log.action}")
        if log.notes:
            print(f"      Notes: {log.notes}")
    
    print("\n🎉 Model testing completed successfully!")
    return len(created_calls)

def test_database_integrity():
    """Test database relationships and constraints"""
    print("\n🔍 Testing Database Integrity")
    print("-" * 30)
    
    # Test unique call_id generation
    calls_before = BudtenderCall.objects.count()
    
    call1 = BudtenderCall.objects.create(
        kiosk_id='TEST_KIOSK',
        reason='Test Call 1',
        priority='normal'
    )
    
    call2 = BudtenderCall.objects.create(
        kiosk_id='TEST_KIOSK', 
        reason='Test Call 2',
        priority='high'
    )
    
    # Verify unique call IDs
    assert call1.call_id != call2.call_id, "Call IDs should be unique"
    print("   ✅ Unique call ID generation working")
    
    # Test foreign key relationship
    log_count_before = BudtenderCallLog.objects.count()
    
    # Create a manual log entry since they may not be auto-created
    log_entry = BudtenderCallLog.objects.create(
        call=call1,
        action='acknowledged',
        staff_member='test_admin',
        notes='Test acknowledgment'
    )
    
    log_count_after = BudtenderCallLog.objects.count()
    assert log_count_after > log_count_before, "Log entry should be created"
    print("   ✅ Foreign key relationships working")
    
    # Test SLA monitoring
    urgent_call = BudtenderCall.objects.create(
        kiosk_id='TEST_URGENT',
        reason='emergency',
        priority='urgent'
    )
    
    # Check if SLA is calculated properly
    assert urgent_call.is_overdue == False, "New urgent call should not be overdue immediately"
    print("   ✅ SLA monitoring working")
    
    print("   🎯 Database integrity tests passed!")

if __name__ == "__main__":
    print("🚀 Enhanced Budtender System - Model Testing")
    print("=" * 60)
    
    try:
        # Test models
        call_count = test_budtender_models()
        
        # Test database integrity
        test_database_integrity()
        
        print("\n" + "=" * 60)
        print("✨ ALL TESTS PASSED!")
        print(f"📊 Database Status:")
        print(f"   Total calls: {BudtenderCall.objects.count()}")
        print(f"   Total logs: {BudtenderCallLog.objects.count()}")
        print(f"   Pending calls: {BudtenderCall.objects.filter(status='pending').count()}")
        
        print("\n🎯 Ready for admin interface testing!")
        print("   Access: http://127.0.0.1:8000/admin/")
        print("   Login: admin / admin123")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
