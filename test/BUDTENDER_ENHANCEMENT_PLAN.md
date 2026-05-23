# Enhanced Budtender Call System Implementation

## 1. Add Call Reasons to Models
```python
# In kiosk/models.py
class BudtenderCall(models.Model):
    REASON_CHOICES = [
        ('product_help', 'Product Information & Recommendations'),
        ('dosage_help', 'Dosage & Consumption Guidance'), 
        ('technical_issue', 'Kiosk Technical Issue'),
        ('payment_issue', 'Payment Problem'),
        ('general_help', 'General Assistance'),
        ('emergency', 'Emergency Assistance'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('normal', 'Normal Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Response'),
        ('acknowledged', 'Acknowledged by Budtender'),
        ('in_progress', 'Assistance in Progress'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    kiosk_id = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100, blank=True)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default='general_help')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    customer_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    response_time = models.DurationField(null=True, blank=True)
    
    budtender_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
```

## 2. Enhanced Call Button with Reason Selection
```html
<!-- Enhanced floating button with dropdown -->
<div class="budtender-call-widget">
    <button id="callBudtenderBtn" class="budtender-float">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
        </svg>
        <span>Call Budtender</span>
    </button>
    
    <!-- Reason Selection Modal -->
    <div id="budtenderModal" class="budtender-modal hidden">
        <div class="modal-content">
            <h3>How can we help you?</h3>
            <div class="reason-buttons">
                <button class="reason-btn" data-reason="product_help">
                    🌿 Product Information
                </button>
                <button class="reason-btn" data-reason="dosage_help">
                    📏 Dosage Guidance
                </button>
                <button class="reason-btn" data-reason="technical_issue">
                    ⚙️ Technical Issue
                </button>
                <button class="reason-btn" data-reason="payment_issue">
                    💳 Payment Problem
                </button>
                <button class="reason-btn" data-reason="general_help">
                    ❓ General Help
                </button>
                <button class="reason-btn emergency" data-reason="emergency">
                    🚨 Emergency
                </button>
            </div>
            <button id="cancelCall" class="cancel-btn">Cancel</button>
        </div>
    </div>
</div>
```

## 3. Enhanced Backend with Call Tracking
```python
# Enhanced view in kiosk/views.py
@age_verified_required
@csrf_exempt
@require_POST
def call_budtender_view(request):
    """Enhanced budtender call with reason tracking"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        # Create call record
        call = BudtenderCall.objects.create(
            kiosk_id=data.get('kiosk_id', settings.KIOSK_CONFIG['KIOSK_ID']),
            session_id=data.get('session_id', 'anonymous'),
            reason=data.get('reason', 'general_help'),
            customer_message=data.get('message', ''),
            priority='urgent' if data.get('reason') == 'emergency' else 'normal'
        )
        
        # Send WebSocket notification with enhanced data
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'budtender_calls',
            {
                'type': 'budtender.call.notification',
                'call_id': call.id,
                'kiosk_id': call.kiosk_id,
                'reason': call.reason,
                'priority': call.priority,
                'timestamp': call.created_at.isoformat(),
                'message': get_reason_display(call.reason),
                'message_type': 'budtender.call'
            }
        )
        
        # Trigger additional alerts for high priority
        if call.priority in ['high', 'urgent']:
            # Send SMS/email to budtender if configured
            try:
                send_priority_alert(call)
            except Exception as e:
                logger.warning(f"Failed to send priority alert: {e}")
        
        return JsonResponse({
            'success': True,
            'call_id': call.id,
            'message': f'Budtender notified for {get_reason_display(call.reason)}'
        })
        
    except Exception as e:
        logger.error(f"Budtender call error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to notify budtender. Please visit the counter.'
        }, status=500)

def get_reason_display(reason):
    reasons = {
        'product_help': 'Product Information & Recommendations',
        'dosage_help': 'Dosage & Consumption Guidance',
        'technical_issue': 'Kiosk Technical Issue',
        'payment_issue': 'Payment Problem',
        'general_help': 'General Assistance',
        'emergency': 'EMERGENCY ASSISTANCE',
    }
    return reasons.get(reason, 'General Assistance')
```

## 4. Physical Hardware Integration Options

### Option A: Raspberry Pi GPIO
```python
# Hardware alert system for Raspberry Pi
class HardwareAlerts:
    def __init__(self):
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.gpio_available = True
            self.setup_pins()
        except ImportError:
            self.gpio_available = False
    
    def setup_pins(self):
        if not self.gpio_available:
            return
            
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(18, self.GPIO.OUT)  # Buzzer
        self.GPIO.setup(24, self.GPIO.OUT)  # LED
        
    def trigger_alert(self, priority='normal'):
        if not self.gpio_available:
            return
            
        patterns = {
            'normal': [(0.3, 0.2)] * 2,      # 2 beeps
            'high': [(0.2, 0.1)] * 3,        # 3 quick beeps  
            'urgent': [(0.5, 0.1)] * 5,      # 5 long beeps
        }
        
        pattern = patterns.get(priority, patterns['normal'])
        
        for on_time, off_time in pattern:
            self.GPIO.output(18, self.GPIO.HIGH)
            self.GPIO.output(24, self.GPIO.HIGH)
            time.sleep(on_time)
            self.GPIO.output(18, self.GPIO.LOW)
            self.GPIO.output(24, self.GPIO.LOW)
            time.sleep(off_time)
```

### Option B: USB/Serial Device Integration
```python
# For USB buzzers, LED strips, or serial devices
class USBAlerts:
    def __init__(self, device_path='/dev/ttyUSB0'):
        try:
            import serial
            self.serial = serial.Serial(device_path, 9600)
            self.available = True
        except:
            self.available = False
    
    def trigger_alert(self, priority='normal'):
        if not self.available:
            return
            
        commands = {
            'normal': b'BEEP:2\n',
            'high': b'BEEP:3\n', 
            'urgent': b'BEEP:5,LED:FLASH\n'
        }
        
        command = commands.get(priority, commands['normal'])
        self.serial.write(command)
```

## 5. Enhanced Dashboard Features

### Real-time Status Updates
```javascript
// Enhanced WebSocket handling in budtender dashboard
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    
    if (data.type === 'budtender_call') {
        // Enhanced notification with reason and priority
        createEnhancedNotification(data);
        
        // Priority-based alerts
        if (data.priority === 'urgent') {
            triggerUrgentAlert();
        }
        
        // Play different sounds based on reason
        playNotificationSound(data.reason);
    }
};

function createEnhancedNotification(data) {
    const priorityColors = {
        'urgent': 'bg-red-100 border-red-500',
        'high': 'bg-orange-100 border-orange-500', 
        'normal': 'bg-blue-100 border-blue-500',
        'low': 'bg-gray-100 border-gray-500'
    };
    
    const reasonIcons = {
        'product_help': '🌿',
        'dosage_help': '📏',
        'technical_issue': '⚙️',
        'payment_issue': '💳',
        'general_help': '❓',
        'emergency': '🚨'
    };
    
    // Create notification with enhanced styling based on priority and reason
    // ... notification creation code ...
}
```

## 6. Analytics and Reporting
```python
# Add analytics views
@staff_member_required
def budtender_analytics_view(request):
    """Analytics dashboard for budtender calls"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    stats = {
        'total_calls_today': BudtenderCall.objects.filter(created_at__date=today).count(),
        'average_response_time': BudtenderCall.objects.filter(
            response_time__isnull=False
        ).aggregate(avg=models.Avg('response_time'))['avg'],
        'reason_breakdown': BudtenderCall.objects.filter(
            created_at__date__gte=week_ago
        ).values('reason').annotate(count=models.Count('id')),
        'peak_hours': BudtenderCall.objects.filter(
            created_at__date=today
        ).extra(
            select={'hour': 'EXTRACT(hour FROM created_at)'}
        ).values('hour').annotate(count=models.Count('id')).order_by('hour')
    }
    
    return render(request, 'kiosk/budtender_analytics.html', {'stats': stats})
```
