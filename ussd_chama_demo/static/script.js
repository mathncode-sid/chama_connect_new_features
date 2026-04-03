// USSD Simulator
let currentSessionId = null;
let isSessionActive = false;
let sessionHistory = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    setupEventListeners();
});

function setupEventListeners() {
    const userInput = document.getElementById('userInput');
    
    // Enable/disable send button based on input
    userInput.addEventListener('input', function() {
        document.getElementById('sendBtn').disabled = !isSessionActive || this.value.trim() === '';
    });
}

function loadStats() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('groupBalance').textContent = `Ksh ${data.balance}`;
            document.getElementById('memberCount').textContent = data.memberCount;
            document.getElementById('status').textContent = 'Active';
        })
        .catch(error => console.error('Error loading stats:', error));
}

function startUSSD() {
    const phoneNumber = prompt('Enter phone number (default: 254700000000):', '254700000000');
    if (phoneNumber === null) return;

    fetch('/api/ussd/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ phoneNumber: phoneNumber })
    })
    .then(response => response.json())
    .then(data => {
        currentSessionId = data.sessionId;
        isSessionActive = true;
        sessionHistory = [];
        
        // Update UI
        document.getElementById('sessionId').textContent = `Session: ${currentSessionId.substring(0, 8)}...`;
        document.getElementById('phoneNumber').textContent = `📱 ${phoneNumber}`;
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('endBtn').disabled = false;
        document.getElementById('userInput').disabled = false;
        
        displayMessage(data.message, 'CON');
        addToHistory('SYSTEM', `Session started with ${phoneNumber}`);
    })
    .catch(error => {
        console.error('Error starting USSD:', error);
        alert('Error starting USSD session');
    });
}

function sendChoiceToUSSD() {
    const userInput = document.getElementById('userInput').value.trim();
    
    if (!userInput) {
        alert('Please enter a choice or value');
        return;
    }

    // Show sending state
    document.getElementById('sendBtn').classList.add('sending');
    document.getElementById('sendBtn').disabled = true;

    fetch('/api/ussd/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sessionId: currentSessionId,
            choice: userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        addToHistory('USER', userInput);
        displayMessage(data.message, data.status);
        addToHistory('USSD', data.message);
        
        document.getElementById('userInput').value = '';
        
        if (data.status === 'END') {
            isSessionActive = false;
            document.getElementById('sendBtn').disabled = true;
        } else {
            document.getElementById('sendBtn').disabled = false;
        }
        
        document.getElementById('sendBtn').classList.remove('sending');
    })
    .catch(error => {
        console.error('Error sending USSD:', error);
        alert('Error processing USSD request');
        document.getElementById('sendBtn').classList.remove('sending');
        document.getElementById('sendBtn').disabled = false;
    });
}

function displayMessage(message, status) {
    const screenDisplay = document.getElementById('screenDisplay');
    
    let statusText = status === 'CON' ? 'CONTINUE' : 'END SESSION';
    let displayContent = `<div style="margin-bottom: 20px;">
        <div style="color: #00ff00; margin-bottom: 10px; font-size: 0.8em;">[${statusText}]</div>
        <div>${message}</div>
    </div>`;
    
    screenDisplay.innerHTML = displayContent;
    screenDisplay.scrollTop = screenDisplay.scrollHeight;
}

function endUSSD() {
    if (confirm('Are you sure you want to end this USSD session?')) {
        addToHistory('SYSTEM', 'Session ended by user');
        
        document.getElementById('screenDisplay').innerHTML = `
            <div class="welcome-message">
                <p>Session Ended</p>
                <p style="font-size: 0.9em; color: #888;">Thank you for using ChamaConnect USSD</p>
                <button class="btn-primary" onclick="resetSession()">Start New Session</button>
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
}

function resetSession() {
    isSessionActive = false;
    currentSessionId = null;
    sessionHistory = [];
    
    document.getElementById('screenDisplay').innerHTML = `
        <div class="welcome-message">
            <p>Ready to start USSD session...</p>
            <button class="btn-primary" onclick="startUSSD()">Start USSD Session</button>
        </div>
    `;
    
    document.getElementById('userInput').value = '';
    document.getElementById('userInput').disabled = true;
    document.getElementById('sendBtn').disabled = true;
    document.getElementById('endBtn').disabled = true;
    document.getElementById('startBtn').style.display = 'block';
    document.getElementById('startBtn').textContent = 'Start USSD Session';
    document.getElementById('sessionId').textContent = '';
    document.getElementById('phoneNumber').textContent = '📱 254700000000';
    
    updateHistory();
}

function addToHistory(type, message) {
    const timestamp = new Date().toLocaleTimeString();
    sessionHistory.push({
        time: timestamp,
        type: type,
        message: message
    });
    updateHistory();
}

function updateHistory() {
    const historyContent = document.getElementById('historyContent');
    
    if (sessionHistory.length === 0) {
        historyContent.innerHTML = '<p class="empty-state">No session history yet</p>';
        return;
    }
    
    let html = '';
    sessionHistory.forEach(item => {
        let typeClass = item.type === 'USER' ? 'user-input' : 
                       item.type === 'USSD' ? 'ussd-response' : '';
        
        html += `<div class="history-item">
            <span style="color: #999; font-size: 0.8em;">[${item.time}]</span>
            <div class="${typeClass}"><strong>${item.type}:</strong> ${escapeHtml(item.message)}</div>
        </div>`;
    });
    
    historyContent.innerHTML = html;
    historyContent.scrollTop = historyContent.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        if (!document.getElementById('sendBtn').disabled && isSessionActive) {
            sendChoiceToUSSD();
        }
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Refresh stats every 10 seconds
setInterval(loadStats, 10000);
