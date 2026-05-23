#!/usr/bin/env python3
"""
Test Script for Admin Sound Notifications
This script will test the budtender call notification system with sound alerts.
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

def create_test_call():
    """Create a test budtender call"""
    call = BudtenderCall.objects.create(
        call_id=uuid.uuid4(),
        kiosk_id='ADMIN_SOUND_TEST',
        session_id='test_session_admin_sound',
        reason='product_help',
        priority='high',
        customer_message='Testing admin sound notification system - Please respond!'
    )
    return call

def send_websocket_notification(call):
    """Send WebSocket notification to admin interface"""
    try:
        # Create call data for WebSocket
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
        
        # Send to admin interface
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'budtender_calls',
            {
                'type': 'budtender_call_notification',
                'call': call_data,
                'message_type': 'budtender_call'
            }
        )
        
        print(f"✅ WebSocket notification sent for call {call.call_id}")
        return True
        
    except Exception as e:
        print(f"❌ WebSocket notification failed: {e}")
        return False

def main():
    print("🔊 ADMIN SOUND NOTIFICATION TEST")
    print("=" * 50)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📞 Creating test budtender call...")
    call = create_test_call()
    print(f"   ✅ Created call: {call.call_id}")
    print(f"   📍 Kiosk: {call.kiosk_id}")
    print(f"   🎯 Reason: {call.get_reason_display()}")
    print(f"   ⚡ Priority: {call.get_priority_display()}")
    print()
    
    print("📡 Sending WebSocket notification...")
    success = send_websocket_notification(call)
    
    if success:
        print("🎉 NOTIFICATION SENT SUCCESSFULLY!")
        print()
        print("🔊 Check the admin interface for:")
        print("   • Sound notification (beep/chime)")
        print("   • Popup notification overlay")
        print("   • Browser notification (if permission granted)")
        print()
        print("🌐 Admin Interface URL:")
        print("   http://127.0.0.1:8002/admin/kiosk/budtendercall/")
        print()
        print("💡 The notification should appear immediately if:")
        print("   • WebSocket connection is active")
        print("   • Admin interface is open in browser")
        print("   • JavaScript notifications are enabled")
        
    else:
        print("❌ Failed to send notification")
        
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
