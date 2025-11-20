/**
 * Density Chart Module
 * Handles prime density chart generation
 */

const generateDensityBtn = document.getElementById('generateDensityBtn');
const densityIntervalInput = document.getElementById('densityInterval');
const densityMaxRangeInput = document.getElementById('densityMaxRange');
const densityPreview = document.getElementById('densityPreview');
const densityImage = document.getElementById('densityImage');

// Generate Density Chart Button Handler
generateDensityBtn.addEventListener('click', async () => {
    const interval = parseInt(densityIntervalInput.value);
    const maxRange = densityMaxRangeInput.value ? parseInt(densityMaxRangeInput.value) : null;

    if (isNaN(interval) || interval < 1000) {
        window.appUtils.showAlert('densityAlert', 'Przedział musi być co najmniej 1000', 'error');
        return;
    }

    // Disable button and show loading
    generateDensityBtn.disabled = true;
    generateDensityBtn.innerHTML = '<span class="spinner"></span><span>Generowanie...</span>';
    window.appUtils.hideAlert('densityAlert');
    densityPreview.classList.remove('active');

    try {
        const response = await fetch('/api/density-chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ interval, max_range: maxRange })
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Generation failed');
        }

        // Display chart
        densityImage.src = `data:image/png;base64,${result.data}`;
        densityPreview.classList.add('active');

        window.appUtils.showAlert('densityAlert',
            `Wykres wygenerowany! Przedział: ${window.appUtils.formatNumber(result.interval)}`,
            'success');

    } catch (error) {
        console.error('Error generating density chart:', error);
        window.appUtils.showAlert('densityAlert', `Błąd: ${error.message}`, 'error');
    } finally {
        generateDensityBtn.disabled = false;
        generateDensityBtn.innerHTML = '<span>📊</span><span>Generuj Wykres</span>';
    }
});
