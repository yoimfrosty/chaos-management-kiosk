// Enhanced Admin JavaScript for Budtender Calls with Real-time Notifications
(function () {
  "use strict";

  // Configuration
  const config = {
    wsProtocol: window.location.protocol === "https:" ? "wss:" : "ws:",
    wsHost: window.location.host,
    refreshInterval: 30000, // 30 seconds
    notificationDuration: 10000, // 10 seconds
    maxNotifications: 3,
    soundEnabled: true,
    popupEnabled: true,
  };

  // Global variables
  let socket = null;
  let reconnectAttempts = 0;
  let maxReconnectAttempts = 5;
  let reconnectInterval = 5000;
  let notificationQueue = [];
  let audioContext = null;
  let notificationCount = 0;
  let notificationAudio = null;

  // Initialize when DOM is ready
  document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin JS Loading...");
    initializeBudtenderCallAdmin();

    // Also initialize on any admin page, not just budtender call pages
    if (window.location.pathname.includes("/admin/")) {
      console.log("Admin page detected, initializing notifications...");
      initializeWebSocket();
      initializeNotificationSound();
      initializeAudioContext();
      requestNotificationPermission();
      addSoundToggle();
    }
  });

  function initializeBudtenderCallAdmin() {
    console.log("Initializing Budtender Call Admin...");

    // Initialize audio for notifications
    initializeNotificationSound();

    // Initialize WebSocket connection
    initializeWebSocket();

    // Initialize audio context (requires user interaction)
    initializeAudioContext();

    // Set up quick action buttons
    setupQuickActions();

    // Set up periodic refresh
    setupPeriodicRefresh();

    // Set up notification permissions
    requestNotificationPermission();

    // Add visual indicators
    enhanceCallDisplay();

    // Add enable/disable sound button
    addSoundToggle();
  }

  function initializeNotificationSound() {
    // Create audio element for notification sound
    notificationAudio = new Audio();

    // Try different sound sources (using data URLs for built-in sounds)
    const sounds = [
      "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmJPCkGs5+ScUhILWq7g7qhWFk8+e8jg5Z1SLwxOmeHQv2FKCyq13+eTXBgOZYPO9d2JQQwKgxgAAAAAAOABAQFgAC",
      "data:audio/wav;base64,UklGRjIAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQ4AAAB+f3+AgYGBf35+fn6Af4CBgYF+fn5+gH+AgYGBfn5+foB/gIGBgX5+fn6Af4CBgYF+fn5+gH+AgYGBfn5+foB/",
    ];

    notificationAudio.src = sounds[0];
    notificationAudio.volume = 0.7;
    notificationAudio.preload = "auto";

    // Fallback: create beep sound with Web Audio API
    notificationAudio.onerror = function () {
      console.log("Using Web Audio API for notification sound");
    };
  }

  function initializeWebSocket() {
    const wsUrl = `${config.wsProtocol}//${config.wsHost}/ws/budtender-calls/`;

    try {
      socket = new WebSocket(wsUrl);

      socket.onopen = function (event) {
        console.log("WebSocket connected for budtender notifications");
        reconnectAttempts = 0;
        showConnectionStatus("Connected", "success");
      };

      socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };

      socket.onclose = function (event) {
        console.log("WebSocket connection closed");
        showConnectionStatus("Disconnected", "error");
        attemptReconnect();
      };

      socket.onerror = function (error) {
        console.error("WebSocket error:", error);
        showConnectionStatus("Connection Error", "error");
      };
    } catch (error) {
      console.error("Failed to initialize WebSocket:", error);
    }
  }

  function handleWebSocketMessage(data) {
    console.log("Received WebSocket message:", data);

    if (data.type === "budtender_call") {
      handleNewCall(data.call);
    } else if (data.type === "call_update") {
      handleCallUpdate(data.call);
    }
  }

  function handleNewCall(callData) {
    console.log("New budtender call received:", callData);

    // Play notification sound
    playNotificationSound();

    // Show popup notification
    showPopupNotification(callData);

    // Show browser notification if permitted
    showBrowserNotification(callData);

    // Refresh the page to show new call
    setTimeout(() => {
      window.location.reload();
    }, 1000);
  }

  function handleCallUpdate(callData) {
    // Update the specific row if it exists
    updateCallRow(callData);
  }

  function playNotificationSound() {
    if (!config.soundEnabled) return;

    try {
      // Try to play the audio file first
      if (notificationAudio && notificationAudio.readyState >= 2) {
        notificationAudio.currentTime = 0;
        notificationAudio.play().catch((e) => {
          console.log("Audio play failed, using Web Audio API fallback");
          playBeepSound();
        });
      } else {
        playBeepSound();
      }
    } catch (error) {
      console.log("Sound notification failed:", error);
      playBeepSound();
    }
  }

  function playBeepSound() {
    // Create beep sound using Web Audio API
    try {
      if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }

      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      oscillator.frequency.value = 800; // 800 Hz tone
      oscillator.type = "sine";

      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(
        0.01,
        audioContext.currentTime + 0.5
      );

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.5);
    } catch (error) {
      console.log("Web Audio API beep failed:", error);
    }
  }

  function showPopupNotification(callData) {
    if (!config.popupEnabled) return;

    // Create popup overlay
    const overlay = document.createElement("div");
    overlay.className = "budtender-notification-overlay";
    overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 10000;
            display: flex;
            justify-content: center;
            align-items: center;
        `;

    // Create popup content
    const popup = document.createElement("div");
    popup.className = "budtender-notification-popup";
    popup.style.cssText = `
            background: white;
            border-radius: 8px;
            padding: 20px;
            max-width: 400px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            text-align: center;
            border: 3px solid #ff4444;
            animation: pulse 1s infinite;
        `;

    const priority = callData.priority || "normal";
    const reason = callData.reason_display || "General Assistance";
    const kioskId = callData.kiosk_id || "Unknown";

    popup.innerHTML = `
            <div style="font-size: 24px; margin-bottom: 15px;">🚨</div>
            <h2 style="color: #ff4444; margin: 0 0 10px 0;">Customer Needs Assistance!</h2>
            <p style="margin: 10px 0; font-size: 16px;"><strong>Kiosk:</strong> ${kioskId}</p>
            <p style="margin: 10px 0; font-size: 16px;"><strong>Reason:</strong> ${reason}</p>
            <p style="margin: 10px 0; font-size: 16px;"><strong>Priority:</strong> ${priority.toUpperCase()}</p>
            <div style="margin-top: 20px;">
                <button id="acknowledgeBtn" style="
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 5px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                ">Acknowledge</button>
                <button id="dismissBtn" style="
                    background: #f44336;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 5px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                ">Dismiss</button>
            </div>
        `;

    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    // Add CSS animation
    const style = document.createElement("style");
    style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        `;
    document.head.appendChild(style);

    // Handle button clicks
    popup.querySelector("#acknowledgeBtn").onclick = function () {
      document.body.removeChild(overlay);
      // Redirect to call details
      if (callData.call_id) {
        window.location.href = `/admin/kiosk/budtendercall/?q=${callData.call_id}`;
      }
    };

    popup.querySelector("#dismissBtn").onclick = function () {
      document.body.removeChild(overlay);
    };

    // Auto-dismiss after 15 seconds
    setTimeout(() => {
      if (document.body.contains(overlay)) {
        document.body.removeChild(overlay);
      }
    }, 15000);
  }

  function showBrowserNotification(callData) {
    if (Notification.permission === "granted") {
      const notification = new Notification("Budtender Call Request", {
        body: `Customer needs assistance at Kiosk ${
          callData.kiosk_id || "Unknown"
        }: ${callData.reason_display || "General Help"}`,
        icon: "/static/admin/img/icon-alert.svg",
        badge: "/static/admin/img/icon-alert.svg",
        tag: "budtender-call",
        requireInteraction: true,
      });

      notification.onclick = function () {
        window.focus();
        if (callData.call_id) {
          window.location.href = `/admin/kiosk/budtendercall/?q=${callData.call_id}`;
        }
      };
    }
  }

  function setupQuickActions() {
    document.addEventListener("click", function (event) {
      if (event.target.classList.contains("acknowledge-btn")) {
        event.preventDefault();
        const callId = event.target.getAttribute("data-call-id");
        performQuickAction(callId, "acknowledge", event.target);
      } else if (event.target.classList.contains("start-btn")) {
        event.preventDefault();
        const callId = event.target.getAttribute("data-call-id");
        performQuickAction(callId, "start", event.target);
      } else if (event.target.classList.contains("resolve-btn")) {
        event.preventDefault();
        const callId = event.target.getAttribute("data-call-id");
        performQuickAction(callId, "resolve", event.target);
      }
    });
  }

  function performQuickAction(callId, action, button) {
    // Show loading state
    const originalText = button.textContent;
    button.textContent = "Processing...";
    button.disabled = true;

    // Send action via WebSocket or AJAX
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(
        JSON.stringify({
          type: "call_action",
          call_id: callId,
          action: action,
          staff_member: getCurrentUserName(),
        })
      );
    }

    // Restore button after delay (will be updated by WebSocket response)
    setTimeout(() => {
      button.textContent = originalText;
      button.disabled = false;
      refreshAdminList();
    }, 2000);
  }

  function getCurrentUserName() {
    // Try to get current user name from Django admin interface
    const userTools = document.getElementById("user-tools");
    if (userTools) {
      const userLink = userTools.querySelector("a");
      if (userLink) {
        return userLink.textContent.trim();
      }
    }
    return "Admin User";
  }

  function initializeAudioContext() {
    // Initialize on first user interaction
    document.addEventListener(
      "click",
      function initAudio() {
        if (!audioContext) {
          try {
            audioContext = new (window.AudioContext ||
              window.webkitAudioContext)();
            console.log("Audio context initialized");
          } catch (error) {
            console.warn("Could not initialize audio context:", error);
          }
        }
        document.removeEventListener("click", initAudio);
      },
      { once: true }
    );
  }

  function requestNotificationPermission() {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission().then(function (permission) {
        console.log("Notification permission:", permission);
      });
    }
  }

  function showConnectionStatus(status, type) {
    const indicator = document.createElement("div");
    indicator.className = "audio-indicator";
    indicator.textContent = `🔗 ${status}`;
    indicator.style.background = type === "success" ? "#4CAF50" : "#f44336";

    document.body.appendChild(indicator);

    setTimeout(() => {
      if (indicator.parentElement) {
        indicator.remove();
      }
    }, 3000);
  }

  function showAudioIndicator() {
    const indicator = document.createElement("div");
    indicator.className = "audio-indicator";
    indicator.textContent = "🔊 Notification";

    document.body.appendChild(indicator);

    setTimeout(() => {
      if (indicator.parentElement) {
        indicator.remove();
      }
    }, 2000);
  }

  function attemptReconnect() {
    if (reconnectAttempts < maxReconnectAttempts) {
      reconnectAttempts++;
      console.log(
        `Attempting to reconnect (${reconnectAttempts}/${maxReconnectAttempts})...`
      );

      setTimeout(() => {
        initializeWebSocket();
      }, reconnectInterval * reconnectAttempts);
    } else {
      console.log("Max reconnection attempts reached");
      showConnectionStatus("Connection Failed", "error");
    }
  }

  function setupPeriodicRefresh() {
    // Refresh the admin list periodically to catch any missed updates
    setInterval(() => {
      if (document.visibilityState === "visible") {
        refreshAdminList();
      }
    }, config.refreshInterval);
  }

  function refreshAdminList() {
    // Only refresh if we're on the budtender call list page
    if (
      window.location.pathname.includes("/budtendercall/") &&
      !window.location.pathname.includes("/add/") &&
      !window.location.pathname.includes("/change/")
    ) {
      // Use a gentle page refresh that preserves scroll position
      const scrollPosition = window.pageYOffset;
      window.location.reload();

      // Restore scroll position after reload
      window.addEventListener(
        "load",
        function () {
          window.scrollTo(0, scrollPosition);
        },
        { once: true }
      );
    }
  }

  function updateCallRow(callData) {
    // Find and update the specific call row in the admin list
    const rows = document.querySelectorAll("table tbody tr");
    rows.forEach((row) => {
      const callIdCell = row.querySelector("td:first-child");
      if (
        callIdCell &&
        callIdCell.textContent.includes(callData.call_id.substring(0, 8))
      ) {
        // Update the row with new data
        highlightUpdatedRow(row);
      }
    });
  }

  function highlightUpdatedRow(row) {
    row.style.backgroundColor = "#e3f2fd";
    row.style.transition = "background-color 0.5s ease";

    setTimeout(() => {
      row.style.backgroundColor = "";
    }, 2000);
  }

  function enhanceCallDisplay() {
    // Add visual enhancements to the call list
    const rows = document.querySelectorAll("table tbody tr");
    rows.forEach((row) => {
      const statusCell = row.querySelector("td:nth-child(2)"); // Assuming status is 2nd column
      if (statusCell) {
        const status = statusCell.textContent.toLowerCase();
        row.classList.add(`call-status-${status.replace(" ", "-")}`);

        // Check if call is overdue (you may need to adjust this logic)
        if (statusCell.textContent.includes("OVERDUE")) {
          row.classList.add("overdue-call");
        }
      }
    });
  }

  function addSoundToggle() {
    // Add sound toggle button to admin interface
    const toggleBtn = document.createElement("button");
    toggleBtn.innerHTML = config.soundEnabled ? "🔊 Sound ON" : "🔇 Sound OFF";
    toggleBtn.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: #007cba;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        `;

    toggleBtn.onclick = function () {
      config.soundEnabled = !config.soundEnabled;
      this.innerHTML = config.soundEnabled ? "🔊 Sound ON" : "🔇 Sound OFF";

      // Test sound when enabled
      if (config.soundEnabled) {
        playNotificationSound();
      }
    };

    document.body.appendChild(toggleBtn);
  }

  // Expose global functions for button actions
  window.notificationCount = 0;
})();
