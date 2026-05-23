(function() {
    let inactivityTimer;
    const inactivityWarningTime = 4.5 * 60 * 1000; // 4.5 minutes to show warning
    const inactivityRedirectTime = 5 * 60 * 1000; // 5 minutes to redirect
    let warningDialog = null;

    function resetInactivityTimer() {
        clearTimeout(inactivityTimer);
        if (warningDialog) {
            warningDialog.remove();
            warningDialog = null;
        }
        inactivityTimer = setTimeout(showInactivityWarning, inactivityWarningTime);
    }

    function showInactivityWarning() {
        clearTimeout(inactivityTimer);
        if (!warningDialog) { // Prevent multiple dialogs
            warningDialog = document.createElement('div');
            warningDialog.className = 'inactivity-warning-overlay';
            warningDialog.innerHTML = `
                <div class="inactivity-warning-dialog">
                    <div class="warning-icon">⏰</div>
                    <h2>Are you still there?</h2>
                    <p>Your session will expire soon due to inactivity.</p>
                    <p>The kiosk will return to the welcome screen in <span id="countdown">30</span> seconds.</p>
                    <button id="stayActiveBtn" class="button-primary">I'm Still Here</button>
                </div>
            `;
            
            // Add styles
            const style = document.createElement('style');
            style.textContent = `
                .inactivity-warning-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    backdrop-filter: blur(4px);
                }
                
                .inactivity-warning-dialog {
                    background: white;
                    padding: 2rem;
                    border-radius: 12px;
                    text-align: center;
                    max-width: 400px;
                    margin: 0 1rem;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                    border: 3px solid var(--ocean-green, #10b981);
                }
                
                .warning-icon {
                    font-size: 3rem;
                    margin-bottom: 1rem;
                    animation: pulse 1s infinite;
                }
                
                .inactivity-warning-dialog h2 {
                    color: #1f2937;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                }
                
                .inactivity-warning-dialog p {
                    color: #6b7280;
                    margin-bottom: 1rem;
                }
                
                #stayActiveBtn {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 8px;
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s ease;
                }
                
                #stayActiveBtn:hover {
                    transform: translateY(-2px);
                }
                
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            `;
            document.head.appendChild(style);
            document.body.appendChild(warningDialog);
            
            // Countdown timer
            let countdown = 30;
            const countdownElement = document.getElementById('countdown');
            const countdownInterval = setInterval(() => {
                countdown--;
                if (countdownElement) {
                    countdownElement.textContent = countdown;
                }
                if (countdown <= 0) {
                    clearInterval(countdownInterval);
                }
            }, 1000);
            
            document.getElementById('stayActiveBtn').addEventListener('click', () => {
                clearInterval(countdownInterval);
                resetInactivityTimer(); // User is active
            });
        }
        // Set timeout for actual redirect
        inactivityTimer = setTimeout(redirectToWelcome, inactivityRedirectTime - inactivityWarningTime);
    }

    function redirectToWelcome() {
        // Clear session and redirect to welcome
        fetch('/clear-session/', { 
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                'Content-Type': 'application/json'
            }
        }).finally(() => {
            window.location.href = "/";
        });
    }

    // Events that count as activity
    window.onload = resetInactivityTimer;
    document.onmousemove = resetInactivityTimer;
    document.onkeypress = resetInactivityTimer;
    document.onclick = resetInactivityTimer;
    document.ontouchstart = resetInactivityTimer;
    document.onscroll = resetInactivityTimer;
    
    // Start the timer when the script loads
    resetInactivityTimer();
})();
