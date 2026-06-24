/**
 * Utility functions for SmartReview
 */

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token && !window.location.pathname.includes('login.html')) {
        window.location.href = '/login.html';
    }
}
checkAuth();

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

// Format currency
function formatCurrency(value) {
    if (value === null || value === undefined || isNaN(value)) {
        return '--';
    }
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(value);
}

// Format percentage
function formatPercentage(value) {
    if (value === null || value === undefined || isNaN(value)) {
        return '--';
    }
    return `${value.toFixed(1)}%`;
}

// Format number
function formatNumber(value, decimals = 2) {
    if (value === null || value === undefined || isNaN(value)) {
        return '--';
    }
    return value.toFixed(decimals);
}

// Format date
function formatDate(dateString) {
    if (!dateString) return '--';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

// Format datetime
function formatDateTime(dateString) {
    if (!dateString) return '--';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Get color based on value (positive/negative)
function getValueColor(value) {
    if (value === null || value === undefined) return '';
    return value >= 0 ? 'positive' : 'negative';
}

// Get color class based on value
function getValueColorClass(value) {
    if (value === null || value === undefined) return '';
    return value >= 0 ? 'text-green' : 'text-red';
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show toast notification
function showToast(message, type = 'info') {
    const container = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i data-lucide="${getToastIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    lucide.createIcons();
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'x-circle',
        warning: 'alert-triangle',
        info: 'info'
    };
    return icons[type] || 'info';
}

// Update current datetime
function updateDateTime() {
    const element = document.getElementById('currentDateTime');
    if (element) {
        const now = new Date();
        element.textContent = now.toLocaleString('fr-FR', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Start datetime update interval
function startDateTimeUpdate() {
    updateDateTime();
    setInterval(updateDateTime, 1000);
}

// Check backend status
async function checkBackendStatus() {
    const statusDot = document.getElementById('backendStatus');
    const statusText = document.getElementById('backendStatusText');
    
    if (!statusDot || !statusText) return;
    
    try {
        const response = await fetch('http://localhost:8001/');
        if (response.ok) {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'En ligne';
        } else {
            throw new Error('Backend not responding');
        }
    } catch (error) {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Hors ligne';
    }
}

// Load accounts into selector
async function loadAccountsIntoSelector() {
    const selector = document.getElementById('activeAccount');
    if (!selector) return;
    
    try {
        const accounts = await API.getAccounts();
        
        selector.innerHTML = accounts.map(a => 
            `<option value="${a.id}">${a.name}</option>`
        ).join('');
        
        // Load saved active account from localStorage
        const savedAccountId = localStorage.getItem('activeAccountId');
        if (savedAccountId && accounts.some(a => a.id === parseInt(savedAccountId))) {
            selector.value = savedAccountId;
        }
        
    } catch (error) {
        console.error('// Error loading accounts - suppressed:', error);
        selector.innerHTML = '<option value="">Erreur de chargement</option>';
    }
}

// Save active account to localStorage
function saveActiveAccount(accountId) {
    localStorage.setItem('activeAccountId', accountId);
}

// Get active account ID
function getActiveAccountId() {
    const selector = document.getElementById('activeAccount');
    return selector ? selector.value : null;
}

// Initialize common functionality
function initializeCommon() {
    startDateTimeUpdate();
    checkBackendStatus();
    loadAccountsIntoSelector();
    
    // Check backend status every 30 seconds
    setInterval(checkBackendStatus, 30000);
    
    // Handle account selector change
    const selector = document.getElementById('activeAccount');
    if (selector) {
        selector.addEventListener('change', (e) => {
            saveActiveAccount(e.target.value);
            // Trigger page-specific reload
            if (typeof onAccountChange === 'function') {
                onAccountChange(e.target.value);
            }
        });
    }
}

// Export functions for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatCurrency,
        formatPercentage,
        formatNumber,
        formatDate,
        formatDateTime,
        getValueColor,
        getValueColorClass,
        debounce,
        showToast,
        updateDateTime,
        startDateTimeUpdate,
        checkBackendStatus,
        loadAccountsIntoSelector,
        saveActiveAccount,
        getActiveAccountId,
        initializeCommon
    };
}
