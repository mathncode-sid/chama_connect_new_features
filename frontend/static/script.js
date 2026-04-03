// Empty States Demo JavaScript

document.addEventListener('DOMContentLoaded', function() {
    setupTabNavigation();
});

function setupTabNavigation() {
    const tabLinks = document.querySelectorAll('.tab-link');
    
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const tabId = this.dataset.tab;
            
            // Remove active from all tabs and links
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.querySelectorAll('.tab-link').forEach(l => {
                l.classList.remove('active');
            });
            
            // Add active to clicked tab and link
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Fetch empty states from API (optional)
async function loadEmptyStates() {
    try {
        const response = await fetch('/api/empty-states');
        const data = await response.json();
        console.log('Empty states loaded:', data);
        return data;
    } catch (error) {
        console.error('Error loading empty states:', error);
    }
}

// Simulate loading state
function simulateLoading(elementSelector, duration = 3000) {
    const element = document.querySelector(elementSelector);
    if (!element) return;
    
    element.classList.add('pulse');
    
    setTimeout(() => {
        element.classList.remove('pulse');
    }, duration);
}

// Show specific empty state
function showEmptyState(stateType) {
    fetch(`/api/empty-states/${stateType}`)
        .then(r => r.json())
        .then(data => {
            console.log(`${stateType} state:`, data.state);
        });
}

// Get loading state
function getLoadingState(stateType) {
    fetch(`/api/loading-state/${stateType}`)
        .then(r => r.json())
        .then(data => {
            console.log(`${stateType} loading:`, data);
        });
}

// Get skeleton loader
function getSkeletonLoader(type) {
    fetch(`/api/skeleton/${type}`)
        .then(r => r.json())
        .then(data => {
            console.log(`${type} skeleton:`, data.html);
        });
}
