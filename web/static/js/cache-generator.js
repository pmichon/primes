/**
 * Cache Generator Module
 * Handles prime cache generation with real-time progress updates
 */

const generateCacheBtn = document.getElementById('generateCacheBtn');
const cacheLimitInput = document.getElementById('cacheLimit');
const progressContainer = document.getElementById('cacheProgress');
const progressFill = document.getElementById('progressFill');
const progressMessage = document.getElementById('progressMessage');
const progressPercent = document.getElementById('progressPercent');

let isGenerating = false;

// Generate Cache Button Handler
generateCacheBtn.addEventListener('click', async () => {
    if (isGenerating) return;

    const limit = parseInt(cacheLimitInput.value);

    if (isNaN(limit) || limit < 100) {
        window.appUtils.showAlert('cacheAlert', 'Proszę podać prawidłowy limit (min. 100)', 'error');
        return;
    }

    // Disable button and show progress
    isGenerating = true;
    generateCacheBtn.disabled = true;
    generateCacheBtn.innerHTML = '<span class="spinner"></span><span>Generowanie...</span>';
    progressContainer.classList.add('active');
    window.appUtils.hideAlert('cacheAlert');

    try {
        // Start generation
        const response = await fetch('/api/generate-cache', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ limit })
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Generation failed');
        }

    } catch (error) {
        console.error('Error generating cache:', error);
        window.appUtils.showAlert('cacheAlert', `Błąd: ${error.message}`, 'error');
        resetGenerateButton();
    }
});

// Socket.IO Progress Updates
window.appUtils.socket.on('cache_progress', (data) => {
    progressFill.style.width = `${data.percent}%`;
    progressMessage.textContent = data.message;
    progressPercent.textContent = `${data.percent}%`;
});

window.appUtils.socket.on('cache_complete', (result) => {
    if (result.success) {
        progressFill.style.width = '100%';
        progressPercent.textContent = '100%';
        progressMessage.textContent = 'Zakończono!';

        window.appUtils.showAlert('cacheAlert', result.message, 'success');
        window.appUtils.loadCacheStats();

        setTimeout(() => {
            progressContainer.classList.remove('active');
            resetGenerateButton();
        }, 2000);
    } else {
        window.appUtils.showAlert('cacheAlert', `Błąd: ${result.error}`, 'error');
        resetGenerateButton();
    }
});

window.appUtils.socket.on('cache_error', (data) => {
    window.appUtils.showAlert('cacheAlert', `Błąd: ${data.error}`, 'error');
    progressContainer.classList.remove('active');
    resetGenerateButton();
});

function resetGenerateButton() {
    isGenerating = false;
    generateCacheBtn.disabled = false;
    generateCacheBtn.innerHTML = '<span>🚀</span><span>Generuj Cache</span>';
    progressFill.style.width = '0%';
}
