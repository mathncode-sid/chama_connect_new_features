// USSD Simulator v2.0 - Enhanced with Error Handling, Loading States, and Interactive Features
let currentSessionId = null;
let isSessionActive = false;
let sessionHistory = [];
let isDemoMode = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    setupKeyboardNavigation();
});

function setupEventListeners() {
    const userInput = document.getElementById('userInput');
    userInput.addEventListener('input', function() {
        document.getElementById('sendBtn').disabled = !isSessionActive || this.value.trim() === '';
    });
}

// Accessibility - Keyboard Navigation
function setupKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        // Alt+S to start session
        if (e.altKey && e.key === 's') {
            startUSSD();
        }
        // Alt+E to end session
        if (e.altKey && e.key === 'e') {
            endUSSD();
        }
    });
}

// Start USSD session
function startUSSD(phoneNumber = null) {
    if (!phoneNumber) {
        phoneNumber = prompt('Enter phone number (default: 254700000000):', '254700000000');
        if (phoneNumber === null) return;
    }

    // Validate phone number
    if (!phoneNumber.match(/^[0-9]{10,}$/)) {
        showError('Invalid phone number. Please enter a valid number.');
        return;
    }

    showLoading(true);

    fetch('/api/ussd/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phoneNumber: phoneNumber })
    })
    .then(response => response.json())
    .then(data => {
        currentSessionId = data.sessionId;
        isSessionActive = true;
        sessionHistory = [];
        
        document.getElementById('sessionId').textContent = `Session: ${currentSessionId.substring(0, 8)}...`;
        document.getElementById('phoneNumber').textContent = `📱 ${phoneNumber}`;
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('endBtn').disabled = false;
        document.getElementById('userInput').disabled = false;
        
        displayMessage(data.message, 'CON');
        addToHistory('SYSTEM', `Session started with ${phoneNumber}`);
        showLoading(false);
        showError(null);
    })
    .catch(error => {
        console.error('Error starting USSD:', error);
        showError('Error starting USSD session. Please try again.');
        showLoading(false);
    });
}

// Send USSD choice
function sendChoiceToUSSD() {
    const userInput = document.getElementById('userInput').value.trim();
    
    if (!userInput) {
        showError('Please enter a choice or value');
        return;
    }

    // Validate input (basic)
    if (!/^[0-9a-zA-Z*#]{1,}$/.test(userInput)) {
        showError('Invalid input. Use only numbers, letters, *, and #');
        return;
    }

    showLoading(true);
    document.getElementById('sendBtn').disabled = true;

    fetch('/api/ussd/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: currentSessionId, choice: userInput })
    })
    .then(response => response.json())
    .then(data => {
        addToHistory('USER', userInput);
        displayMessage(data.message, data.status);
        addToHistory('USSD', data.message);
        
        // Show receipt for contributions
        if (data.status === 'END' && userInput.includes('2')) {
            showReceipt(userInput);
        }
        
        document.getElementById('userInput').value = '';
        
        if (data.status === 'END') {
            isSessionActive = false;
            document.getElementById('sendBtn').disabled = true;
            document.getElementById('endBtn').disabled = true;
        } else {
            document.getElementById('sendBtn').disabled = false;
        }
        
        showLoading(false);
        showError(null);
    })
    .catch(error => {
        console.error('Error sending USSD:', error);
        showError('Error processing USSD request. Please try again.');
        document.getElementById('sendBtn').disabled = false;
        showLoading(false);
    });
}

// Display message on screen
function displayMessage(message, status) {
    const screenDisplay = document.getElementById('screenDisplay');
    const statusText = status === 'CON' ? 'CONTINUE' : 'END SESSION';
    const statusColor = status === 'CON' ? '#10b981' : '#ef4444';
    
    const displayContent = `
        <div style="width: 100%; text-align: center;">
            <div style="color: ${statusColor}; margin-bottom: 15px; font-size: 0.75em; font-weight: bold; letter-spacing: 1px;">[${statusText}]</div>
            <div style="white-space: pre-wrap; word-break: break-word; line-height: 1.6;">${message}</div>
        </div>
    `;
    
    screenDisplay.innerHTML = displayContent;
    screenDisplay.scrollTop = screenDisplay.scrollHeight;
}

// Add to session history
function addToHistory(type, message) {
    const timestamp = new Date().toLocaleTimeString();
    sessionHistory.push({ type, message, timestamp });
    // History display removed - simplified UI only shows phone screen
}

// End USSD session
function endUSSD() {
    if (!confirm('Are you sure you want to end this USSD session?')) return;

    addToHistory('SYSTEM', 'Session ended by user');
    
    document.getElementById('screenDisplay').innerHTML = `
        <div class="welcome-screen">
            <div class="welcome-icon">✓</div>
            <p class="welcome-title">Session Ended</p>
            <p class="welcome-text" style="margin-bottom: 20px;">Thank you for using ChamaConnect USSD</p>
            <button class="btn-primary" onclick="resetSession()" style="font-size: 0.9em;">Start New Session</button>
        </div>
    `;
    
    isSessionActive = false;
    currentSessionId = null;
    document.getElementById('sendBtn').disabled = true;
    document.getElementById('endBtn').disabled = true;
    document.getElementById('userInput').disabled = true;
    document.getElementById('userInput').value = '';
    document.getElementById('startBtn').style.display = 'block';
    document.getElementById('startBtn').textContent = 'Start New Session';
}

// Reset session
function resetSession() {
    currentSessionId = null;
    isSessionActive = false;
    sessionHistory = [];
    isDemoMode = false;
    
    document.getElementById('screenDisplay').innerHTML = `
        <div class="welcome-screen">
            <div class="welcome-icon">📱</div>
            <p class="welcome-title">Ready to Start</p>
            <p class="welcome-text">Start a USSD session to manage your chama group</p>
            <button class="btn-primary" id="startBtn" onclick="startUSSD()">Begin Session</button>
        </div>
    `;
    
    document.getElementById('sendBtn').disabled = true;
    document.getElementById('endBtn').disabled = true;
    document.getElementById('userInput').disabled = true;
    document.getElementById('userInput').value = '';
    document.getElementById('startBtn').style.display = 'block';
    document.getElementById('startBtn').textContent = 'Begin Session';
    showError(null);
}

// Show error message
function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    if (message) {
        errorAlert.textContent = '⚠️ ' + message;
        errorAlert.style.display = 'block';
    } else {
        errorAlert.style.display = 'none';
    }
}

// Show/hide loading indicator
function showLoading(show) {
    // Loading indicator removed from simplified UI
}

// Show receipt modal
function showReceipt(input) {
    const receiptNo = 'RCP' + Date.now().toString().slice(-6);
    const amount = input.split('*')[1] || '0';
    const time = new Date().toLocaleTimeString();
    
    document.getElementById('receiptNo').textContent = receiptNo;
    document.getElementById('receiptAmount').textContent = `Ksh ${amount}`;
    document.getElementById('receiptTime').textContent = time;
    
    document.getElementById('receiptModal').style.display = 'flex';
}

// Close modal
function closeModal() {
    document.getElementById('receiptModal').style.display = 'none';
}

// Demo functions removed - simplified UI focuses on phone simulator only
function closeDemoModal() {
    // Removed
}

function runDemoWalkthrough() {
    // Removed
}


function startDemoWalkthrough() {
    closeDemoModal();
    resetSession();
    isDemoMode = true;
    
    // Auto-run demo sequence
    setTimeout(() => startUSSD('254700000000'), 500);
    
    // View Balance
    setTimeout(() => {
        document.getElementById('userInput').value = '1';
        sendChoiceToUSSD();
    }, 2000);
    
    // Go back to main menu
    setTimeout(() => {
        document.getElementById('userInput').value = '0';
        sendChoiceToUSSD();
    }, 4000);
    
    // Make Contribution
    setTimeout(() => {
        document.getElementById('userInput').value = '2';
        sendChoiceToUSSD();
    }, 5500);
    
    // Enter amount
    setTimeout(() => {
        document.getElementById('userInput').value = '500';
        sendChoiceToUSSD();
    }, 7000);
    
    // Enter name
    setTimeout(() => {
        document.getElementById('userInput').value = 'Alex';
        sendChoiceToUSSD();
    }, 8500);
    
    // End session
    setTimeout(() => {
        endUSSD();
        isDemoMode = false;
        alert('✓ Demo completed! This is how users interact with ChamaConnect via USSD.');
    }, 10000);
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && isSessionActive && !document.getElementById('sendBtn').disabled) {
        sendChoiceToUSSD();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
