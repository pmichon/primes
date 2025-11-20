/**
 * Main Application Logic
 * Handles theme switching, tabs, and cache stats
 */

// Initialize Socket.IO connection
const socket = io();

// Theme Management
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const themeText = document.getElementById('themeText');
const html = document.documentElement;

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);
updateThemeButton(savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeButton(newTheme);
});

function updateThemeButton(theme) {
    if (theme === 'dark') {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light Mode';
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark Mode';
    }
}

// Tab Management
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;

        // Remove active class from all tabs and contents
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        // Add active class to clicked tab and corresponding content
        tab.classList.add('active');
        document.getElementById(`${targetTab}-content`).classList.add('active');
    });
});

// Cache Stats Management
async function loadCacheStats() {
    try {
        const response = await fetch('/api/cache-stats');
        const result = await response.json();

        // Extract data from new API format: {success: true, data: {...}}
        const stats = result.data || result;

        updateCacheStatsUI(stats);
    } catch (error) {
        console.error('Error loading cache stats:', error);
        document.getElementById('cacheStatus').textContent = 'Error';
    }
}

function updateCacheStatsUI(stats) {
    const statusElement = document.getElementById('cacheStatus');
    const countElement = document.getElementById('primesCount');
    const maxValueElement = document.getElementById('maxValue');
    const sizeElement = document.getElementById('cacheSize');

    if (stats.exists) {
        statusElement.textContent = '✓ Exists';
        countElement.textContent = formatNumber(stats.count);
        maxValueElement.textContent = formatNumber(stats.max_value);
        sizeElement.textContent = `${stats.size_mb} MB`;
    } else {
        statusElement.textContent = '✗ Not Found';
        countElement.textContent = '0';
        maxValueElement.textContent = '0';
        sizeElement.textContent = '0 MB';
    }
}

// Utility Functions
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function showAlert(alertId, message, type = 'success') {
    const alert = document.getElementById(alertId);
    const messageElement = document.getElementById(`${alertId}Message`);

    alert.className = `alert alert-${type} active`;
    if (messageElement) {
        messageElement.textContent = message;
    }

    // Auto-hide after 5 seconds
    setTimeout(() => {
        alert.classList.remove('active');
    }, 5000);
}

function hideAlert(alertId) {
    const alert = document.getElementById(alertId);
    alert.classList.remove('active');
}

// Socket.IO Event Handlers
socket.on('connect', () => {
    console.log('Connected to server');
    loadCacheStats();
});

socket.on('connection_response', (data) => {
    console.log('Server response:', data);
});

socket.on('cache_stats_update', (stats) => {
    updateCacheStatsUI(stats);
});

// Load initial stats when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadCacheStats();
});

// Export utility functions for other modules
window.appUtils = {
    formatNumber,
    showAlert,
    hideAlert,
    loadCacheStats,
    socket
};
