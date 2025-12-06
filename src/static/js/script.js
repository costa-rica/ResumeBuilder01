document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const spinnerOverlay = document.getElementById('spinner-overlay');

    if (form) {
        form.addEventListener('submit', function() {
            // Clear spinner text first
            const spinnerText = document.getElementById('spinner-text');
            if (spinnerText) {
                spinnerText.textContent = "";
            }
            
            // Show the spinner
            if (spinnerOverlay) {
                spinnerOverlay.classList.remove('hidden');
            }
            
            if (spinnerText) {
                // Sequence
                // 1. T+3s: Modify Resume
                setTimeout(() => {
                    spinnerText.textContent = "Tailoring your resume to the job description...";
                }, 3000);

                // 2. T+15s: Clear (Step 1 done, wait 4s)
                setTimeout(() => {
                    spinnerText.textContent = "";
                }, 10000);

                // 3. T+19s: Cover Letter
                setTimeout(() => {
                    spinnerText.textContent = "Shakespeare-ing your cover letter...";
                }, 15000);

                // 4. T+31s: Clear (Step 2 done, wait 3s)
                setTimeout(() => {
                    spinnerText.textContent = "";
                }, 20000);

                // 5. T+34s: Scoring
                setTimeout(() => {
                    spinnerText.textContent = "Scoring your resume...";
                }, 21000);
            }
        });
    }
});
