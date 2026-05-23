# Network Testing Guide for Hemp App

## Server Status
✅ Django server is running on: `http://0.0.0.0:8000/`
✅ Your local IP address: `172.20.20.20`
✅ ALLOWED_HOSTS updated to accept network connections

## Testing from Another Device

### Step 1: Ensure Network Connectivity
Make sure both devices (your Mac and the test device) are connected to the same WiFi network.

### Step 2: Access URLs from Other Device
From another device on the same network, you can access:

**Main Kiosk Interface:**
- `http://172.20.20.20:8000/`

**Admin Panel:**
- `http://172.20.20.20:8000/admin/`

**Specific Test Pages:**
- Customer Interface: `http://172.20.20.20:8000/`
- Budtender Calls: `http://172.20.20.20:8000/admin/` (login required)

### Step 3: Test the Budtender Notification System
1. **On the test device (customer side):**
   - Navigate to `http://172.20.20.20:8000/`
   - Click "Call Budtender" button
   - Select a reason (e.g., "Product Information")
   - Listen for immediate audio feedback
   - Look for visual confirmation

2. **On your Mac (admin side):**
   - Keep the admin panel open: `http://localhost:8000/admin/`
   - Listen for admin notification sounds
   - Check for popup notifications

### Step 4: Troubleshooting
If you can't connect from the other device:

1. **Check firewall settings:**
   - macOS Firewall might be blocking connections
   - Go to System Preferences > Security & Privacy > Firewall
   - Allow incoming connections for Python

2. **Verify IP address:**
   - Run `ifconfig` on your Mac to confirm IP hasn't changed
   - Update ALLOWED_HOSTS if needed

3. **Test connectivity:**
   - From the test device, try pinging: `ping 172.20.20.20`
   - If ping fails, check network settings

### Step 5: Testing Features
Test these specific features from the remote device:

- ✅ Age verification dialog
- ✅ Product browsing (Flower, Concentrates, Edibles, etc.)
- ✅ Add items to cart
- ✅ **Budtender call notifications (with sound!)**
- ✅ Checkout process
- ✅ Receipt generation

### WebSocket Testing
The budtender notification system uses WebSockets. Test:
1. Real-time notifications between customer and admin
2. Audio feedback on both sides
3. Visual indicators and animations

### Mobile Testing
If testing on mobile devices:
- iPhones/iPads: Open Safari and navigate to the URL
- Android: Open Chrome/Firefox and navigate to the URL
- Test touch interactions and responsiveness

## Current Configuration
- **Server**: Running on all interfaces (0.0.0.0:8000)
- **Local Access**: http://localhost:8000/
- **Network Access**: http://172.20.20.20:8000/
- **Debug Mode**: Enabled for development
- **WebSockets**: Enabled for real-time notifications
- **Static Files**: Collected and served

## Notes
- Keep the server running while testing
- Both customer and admin interfaces work from remote devices
- Audio notifications work across the network
- All cart functionality is preserved
- Database is shared (SQLite on your Mac)

## Quick Commands
If you need to restart the server:
```bash
cd /Users/uba/Desktop/hemp-app/chaos-magement
python3 manage.py runserver 0.0.0.0:8000
```

If you need to update IP address:
```bash
ifconfig | grep -E "inet .*(192\.168\.|10\.|172\.)" | grep -v 127.0.0.1
```
