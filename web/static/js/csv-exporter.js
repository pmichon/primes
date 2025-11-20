/**
 * CSV Exporter Module
 * Handles CSV export functionality
 */

const exportCsvBtn = document.getElementById('exportCsvBtn');
const exportFormatSelect = document.getElementById('exportFormat');
const chunkSizeInput = document.getElementById('chunkSize');
const chunkSizeGroup = document.getElementById('chunkSizeGroup');

// Show/hide chunk size input based on format selection
exportFormatSelect.addEventListener('change', () => {
    if (exportFormatSelect.value === 'chunks') {
        chunkSizeGroup.style.display = 'block';
    } else {
        chunkSizeGroup.style.display = 'none';
    }
});

// Export CSV Button Handler
exportCsvBtn.addEventListener('click', async () => {
    const format = exportFormatSelect.value;
    const chunkSize = parseInt(chunkSizeInput.value);

    if (format === 'chunks' && (isNaN(chunkSize) || chunkSize < 100000)) {
        window.appUtils.showAlert('exportAlert', 'Rozmiar chunka musi być co najmniej 100000', 'error');
        return;
    }

    // Disable button and show loading
    exportCsvBtn.disabled = true;
    exportCsvBtn.innerHTML = '<span class="spinner"></span><span>Eksportowanie...</span>';
    window.appUtils.hideAlert('exportAlert');

    try {
        const response = await fetch('/api/export-csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ format, chunk_size: chunkSize })
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Export failed');
        }

        window.appUtils.showAlert('exportAlert',
            `Eksport zakończony! Plik: ${result.file}. Możesz pobrać plik z katalogu projektu.`,
            'success');

    } catch (error) {
        console.error('Error exporting CSV:', error);
        window.appUtils.showAlert('exportAlert', `Błąd: ${error.message}`, 'error');
    } finally {
        exportCsvBtn.disabled = false;
        exportCsvBtn.innerHTML = '<span>💾</span><span>Eksportuj CSV</span>';
    }
});

// Verify Cache Button Handler
const verifyCacheBtn = document.getElementById('verifyCacheBtn');

verifyCacheBtn.addEventListener('click', async () => {
    verifyCacheBtn.disabled = true;
    verifyCacheBtn.innerHTML = '<span class="spinner"></span><span>Weryfikacja...</span>';
    window.appUtils.hideAlert('verifyAlert');

    try {
        const response = await fetch('/api/verify-cache');
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Verification failed');
        }

        const stats = result.stats;
        const message = `Cache zweryfikowany pomyślnie! Liczb pierwszych: ${window.appUtils.formatNumber(stats.count)}, Max: ${window.appUtils.formatNumber(stats.max_value)}`;

        window.appUtils.showAlert('verifyAlert', message, 'success');

    } catch (error) {
        console.error('Error verifying cache:', error);
        window.appUtils.showAlert('verifyAlert', `Błąd: ${error.message}`, 'error');
    } finally {
        verifyCacheBtn.disabled = false;
        verifyCacheBtn.innerHTML = '<span>✅</span><span>Weryfikuj Cache</span>';
    }
});
