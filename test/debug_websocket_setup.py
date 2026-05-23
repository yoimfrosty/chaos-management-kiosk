#!/usr/bin/env python3
"""
Debug Channel Layer and WebSocket Setup
"""
import os
import sys
import django

# Setup Django
sys.path.append('/Users/uba/Desktop/hemp-app/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio

def test_channel_layer_sync():
    """Test channel layer synchronously"""
    print("🔧 Testing Channel Layer (Synchronous)")
    print("=" * 50)
    
    try:
        channel_layer = get_channel_layer()
        print(f"✅ Channel layer obtained: {type(channel_layer)}")
        print(f"   Backend: {channel_layer.__class__.__module__}.{channel_layer.__class__.__name__}")
        
        # Test basic functionality
        test_message = {
            'type': 'test_message',
            'content': 'Hello from sync test'
        }
        
        # Try to send a message to a group
        try:
            async_to_sync(channel_layer.group_send)(
                'test_group',
                test_message
            )
            print("✅ Group send executed without error")
        except Exception as e:
            print(f"❌ Group send failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Channel layer test failed: {e}")
        return False

async def test_channel_layer_async():
    """Test channel layer asynchronously"""
    print("\n🔧 Testing Channel Layer (Asynchronous)")
    print("=" * 50)
    
    try:
        channel_layer = get_channel_layer()
        print(f"✅ Channel layer obtained: {type(channel_layer)}")
        
        # Test creating a channel
        channel_name = await channel_layer.new_channel()
        print(f"✅ New channel created: {channel_name}")
        
        # Test group operations
        group_name = 'test_async_group'
        
        # Add channel to group
        await channel_layer.group_add(group_name, channel_name)
        print(f"✅ Channel added to group: {group_name}")
        
        # Send message to group
        test_message = {
            'type': 'test.message',
            'content': 'Hello from async test',
            'timestamp': '2025-06-11T15:10:00'
        }
        
        await channel_layer.group_send(group_name, test_message)
        print("✅ Message sent to group")
        
        # Try to receive message
        try:
            received = await asyncio.wait_for(
                channel_layer.receive(channel_name), 
                timeout=2.0
            )
            print(f"✅ Message received: {received}")
        except asyncio.TimeoutError:
            print("⏰ No message received (this might be expected)")
        
        # Clean up
        await channel_layer.group_discard(group_name, channel_name)
        print("✅ Channel removed from group")
        
        return True
        
    except Exception as e:
        print(f"❌ Async channel layer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_websocket_consumer_import():
    """Test if we can import and inspect the WebSocket consumer"""
    print("\n🔧 Testing WebSocket Consumer Import")
    print("=" * 50)
    
    try:
        from kiosk.consumers import BudtenderConsumer
        print("✅ BudtenderConsumer imported successfully")
        
        # Check consumer methods
        methods = [attr for attr in dir(BudtenderConsumer) if not attr.startswith('_')]
        print(f"   Available methods: {methods}")
        
        # Check specific methods we need
        required_methods = ['connect', 'disconnect', 'budtender_call_notification']
        for method in required_methods:
            if hasattr(BudtenderConsumer, method):
                print(f"   ✅ {method}: Found")
            else:
                print(f"   ❌ {method}: Missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Consumer import failed: {e}")
        return False

def test_routing_configuration():
    """Test WebSocket routing configuration"""
    print("\n🔧 Testing WebSocket Routing Configuration")
    print("=" * 50)
    
    try:
        from kiosk.routing import websocket_urlpatterns
        print("✅ WebSocket URL patterns imported")
        print(f"   Number of patterns: {len(websocket_urlpatterns)}")
        
        for i, pattern in enumerate(websocket_urlpatterns, 1):
            print(f"   {i}. {pattern.pattern.pattern} -> {pattern.callback}")
        
        return True
        
    except Exception as e:
        print(f"❌ Routing test failed: {e}")
        return False

def test_asgi_configuration():
    """Test ASGI configuration"""
    print("\n🔧 Testing ASGI Configuration")
    print("=" * 50)
    
    try:
        from OceanCityKiosk.asgi import application
        print("✅ ASGI application imported")
        print(f"   Application type: {type(application)}")
        
        # Check if it's a ProtocolTypeRouter
        from channels.routing import ProtocolTypeRouter
        if isinstance(application, ProtocolTypeRouter):
            print("✅ Application is ProtocolTypeRouter")
            protocols = list(application.application_mapping.keys())
            print(f"   Supported protocols: {protocols}")
        else:
            print(f"⚠️  Application is {type(application)}, expected ProtocolTypeRouter")
        
        return True
        
    except Exception as e:
        print(f"❌ ASGI configuration test failed: {e}")
        return False

async def main():
    """Run all debugging tests"""
    print("🔍 WEBSOCKET SYSTEM DIAGNOSTIC")
    print("=" * 70)
    
    # Test 1: Channel layer (sync)
    sync_success = test_channel_layer_sync()
    
    # Test 2: Channel layer (async)
    async_success = await test_channel_layer_async()
    
    # Test 3: Consumer import
    consumer_success = test_websocket_consumer_import()
    
    # Test 4: Routing configuration
    routing_success = test_routing_configuration()
    
    # Test 5: ASGI configuration
    asgi_success = test_asgi_configuration()
    
    # Final report
    print("\n" + "=" * 70)
    print("📋 DIAGNOSTIC RESULTS")
    print("=" * 70)
    
    tests = {
        'Channel Layer (Sync)': sync_success,
        'Channel Layer (Async)': async_success,
        'WebSocket Consumer': consumer_success,
        'Routing Configuration': routing_success,
        'ASGI Configuration': asgi_success
    }
    
    all_passed = True
    for test_name, passed in tests.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All diagnostic tests passed!")
        print("   WebSocket infrastructure should be working")
        print("   🔍 The issue might be in the message handling or timing")
    else:
        print("\n⚠️  Some diagnostic tests failed")
        print("   Fix these issues before testing WebSocket notifications")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
