document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const spinnerOverlay = document.getElementById('spinner-overlay');

    if (form) {
        form.addEventListener('submit', function() {
            // Show the spinner
            if (spinnerOverlay) {
                spinnerOverlay.classList.remove('hidden');
            }
        });
    }
});
