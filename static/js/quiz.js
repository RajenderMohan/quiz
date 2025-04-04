document.addEventListener('DOMContentLoaded', function () {
    // Handle choice selection
    document.querySelectorAll('.choice').forEach(choice => {
        choice.addEventListener('click', function () {
            // Remove active class from all choices
            document.querySelectorAll('.choice').forEach(c => {
                c.classList.remove('active');
            });

            // Add active class to selected choice
            this.classList.add('active');

            // Enable submit button
            document.getElementById('submit-btn').disabled = false;
        });
    });

    // Timer functionality
    function startTimer(duration, display) {
        let timer = duration, minutes, seconds;
        const interval = setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                document.getElementById('quiz-form').submit();
            }
        }, 1000);
    }

    // Initialize timer if timer element exists
    const timerDisplay = document.getElementById('time');
    if (timerDisplay) {
        const timeLimit = parseInt(timerDisplay.dataset.timeLimit);
        startTimer(timeLimit, timerDisplay);
    }
});