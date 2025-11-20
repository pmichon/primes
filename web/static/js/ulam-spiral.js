/**
 * Ulam Spiral Module
 * Handles Ulam spiral generation and visualization
 */

const generateSpiralBtn = document.getElementById('generateSpiralBtn');
const spiralSizeInput = document.getElementById('spiralSize');
const spiralFormatSelect = document.getElementById('spiralFormat');
const spiralColorfulCheck = document.getElementById('spiralColorful');
const spiralPreview = document.getElementById('spiralPreview');
const spiralImageContainer = document.getElementById('spiralImageContainer');
const downloadSpiralBtn = document.getElementById('downloadSpiralBtn');

let currentSpiralData = null;
let currentSpiralFormat = 'png';

// Generate Spiral Button Handler
generateSpiralBtn.addEventListener('click', async () => {
    const size = parseInt(spiralSizeInput.value);
    const format = spiralFormatSelect.value;
    const colorful = spiralColorfulCheck.checked;

    if (isNaN(size) || size < 100 || size > 100000000) {
        window.appUtils.showAlert('spiralAlert', 'Rozmiar musi być między 100 a 100,000,000', 'error');
        return;
    }

    // Disable button and show loading
    generateSpiralBtn.disabled = true;
    generateSpiralBtn.innerHTML = '<span class="spinner"></span><span>Generowanie...</span>';
    window.appUtils.hideAlert('spiralAlert');
    spiralPreview.classList.remove('active');

    try {
        const response = await fetch('/api/ulam-spiral', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ n: size, colorful, format })
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Generation failed');
        }

        // Display result
        currentSpiralData = result.data;
        currentSpiralFormat = result.format;
        displaySpiral(result);

        window.appUtils.showAlert('spiralAlert',
            `Spirala wygenerowana! Rozmiar: ${window.appUtils.formatNumber(size)}`,
            'success');

    } catch (error) {
        console.error('Error generating spiral:', error);
        window.appUtils.showAlert('spiralAlert', `Błąd: ${error.message}`, 'error');
    } finally {
        generateSpiralBtn.disabled = false;
        generateSpiralBtn.innerHTML = '<span>🌀</span><span>Generuj Spiralę</span>';
    }
});

function displaySpiral(result) {
    spiralImageContainer.innerHTML = '';

    if (result.format === 'svg') {
        spiralImageContainer.innerHTML = result.data;
        const svg = spiralImageContainer.querySelector('svg');
        if (svg) {
            svg.style.maxWidth = '100%';
            svg.style.height = 'auto';
            svg.style.borderRadius = 'var(--border-radius)';
            svg.style.boxShadow = 'var(--shadow-lg)';
        }
    } else {
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${result.data}`;
        img.alt = 'Spirala Ulama';
        img.className = 'preview-image';
        spiralImageContainer.appendChild(img);
    }

    spiralPreview.classList.add('active');
}

// Download Button Handler
downloadSpiralBtn.addEventListener('click', () => {
    if (!currentSpiralData) return;

    const filename = `spirala_ulama_${spiralSizeInput.value}.${currentSpiralFormat}`;

    if (currentSpiralFormat === 'svg') {
        const blob = new Blob([currentSpiralData], { type: 'image/svg+xml' });
        downloadBlob(blob, filename);
    } else {
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${currentSpiralData}`;
        link.download = filename;
        link.click();
    }
});

function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}
