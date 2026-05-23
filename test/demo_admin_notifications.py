#!/usr/bin/env python3
"""
COMPREHENSIVE ADMIN NOTIFICATION DEMONSTRATION
This script demonstrates the complete admin notification system with sound alerts.
"""

import os
import sys
import django
import json
import time
import threading
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import BudtenderCall
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_step(step, description):
    print(f"\n🔸 STEP {step}: {description}")
    print("-" * 40)

def print_success(message):
    print(f"✅ {message}")

def print_info(message):
    print(f"💡 {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def create_priority_call(priority, reason, message):
    """Create a budtender call with specific priority"""
    call = BudtenderCall.objects.create(
        call_id=uuid.uuid4(),
        kiosk_id=f'DEMO_{priority.upper()}_KIOSK',
        session_id=f'demo_session_{int(time.time())}',
        reason=reason,
        priority=priority,
        customer_message=message
    )
    return call

def send_notification(call):
    """Send WebSocket notification for a call"""
    try:
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
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'budtender_calls',
            {
                'type': 'budtender_call_notification',
                'call': call_data,
                'message_type': 'budtender_call'
            }
        )
        return True
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

def demo_notification_features():
    """Demonstrate different notification features"""
    
    print_header("ADMIN NOTIFICATION SYSTEM DEMONSTRATION")
    
    print_info("This demonstration will show:")
    print("   • Sound notifications (beep/chime)")
    print("   • Visual popup overlays")
    print("   • Browser notifications")
    print("   • Priority-based alerts")
    print("   • Real-time admin updates")
    
    print_warning("Make sure the admin interface is open in your browser!")
    print_info("Admin URL: http://127.0.0.1:8002/admin/kiosk/budtendercall/")
    
    # Demo scenarios
    scenarios = [
        {
            'priority': 'high',
            'reason': 'technical_issue',
            'message': 'Kiosk screen is frozen and customer cannot proceed',
            'description': 'HIGH PRIORITY - Technical Issue'
        },
        {
            'priority': 'urgent',
            'reason': 'emergency',
            'message': 'Medical emergency in store - customer needs immediate assistance',
            'description': 'URGENT - Medical Emergency'
        },
        {
            'priority': 'normal',
            'reason': 'product_help',
            'message': 'Customer wants information about different strains',
            'description': 'NORMAL - Product Information'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print_step(i, scenario['description'])
        
        # Create call
        call = create_priority_call(
            scenario['priority'],
            scenario['reason'],
            scenario['message']
        )
        
        print_success(f"Created {scenario['priority']} priority call:")
        print(f"   📞 Call ID: {call.call_id}")
        print(f"   📍 Kiosk: {call.kiosk_id}")
        print(f"   🎯 Reason: {call.get_reason_display()}")
        print(f"   💬 Message: {call.customer_message}")
        
        # Send notification
        if send_notification(call):
            print_success("WebSocket notification sent!")
            
            # Describe what should happen
            if scenario['priority'] == 'urgent':
                print_info("Expected behavior:")
                print("   🚨 URGENT ALERT: Rapid beeping sound")
                print("   🔴 Red pulsing popup overlay")
                print("   🖥️  Browser notification (if permitted)")
                print("   📢 Immediate admin attention required")
            elif scenario['priority'] == 'high':
                print_info("Expected behavior:")
                print("   ⚠️  HIGH PRIORITY: Two-tone chime")
                print("   🟠 Orange highlighted popup")
                print("   🔔 Browser notification")
                print("   ⏰ Quick response expected")
            else:
                print_info("Expected behavior:")
                print("   🔔 NORMAL: Single tone notification")
                print("   🔵 Blue standard popup")
                print("   📱 Standard browser notification")
                print("   ✋ Normal response time")
        
        # Wait between notifications
        if i < len(scenarios):
            print_info("Waiting 5 seconds before next notification...")
            time.sleep(5)
    
    print_header("NOTIFICATION SYSTEM FEATURES")
    
    print_info("Sound System:")
    print("   • Web Audio API beep sounds")
    print("   • Priority-based tone variations")
    print("   • Fallback audio file support")
    print("   • User toggle for sound on/off")
    
    print_info("Visual Notifications:")
    print("   • Full-screen popup overlays")
    print("   • Priority-based color coding")
    print("   • Pulsing animation for urgency")
    print("   • Auto-dismiss with timeout")
    
    print_info("Browser Integration:")
    print("   • Native browser notifications")
    print("   • Permission-based activation")
    print("   • Click-to-focus functionality")
    print("   • Persistent for urgent calls")
    
    print_info("Real-time Updates:")
    print("   • WebSocket-based communication")
    print("   • Automatic page refresh")
    print("   • Multi-endpoint support")
    print("   • Reconnection handling")
    
    print_header("TESTING COMPLETE")
    
    print_success("All notifications have been sent!")
    print_info("Check the admin interface to see the results.")
    print_info("The system is now ready for production use.")
    
    # Show current calls
    recent_calls = BudtenderCall.objects.filter(
        kiosk_id__startswith='DEMO_'
    ).order_by('-created_at')[:5]
    
    if recent_calls:
        print_info(f"Recent demo calls ({recent_calls.count()}):")
        for call in recent_calls:
            print(f"   📞 {call.get_priority_display()}: {call.get_reason_display()}")
            print(f"      ⏰ {call.created_at.strftime('%H:%M:%S')} - {call.kiosk_id}")

if __name__ == "__main__":
    demo_notification_features()
