let answered = false;

async function handleSubmit() {
    if (answered) {
        // Button is in "Next" mode — advance to next question
        const res = await fetch('/grammar/next', {method: 'POST'});
        const data = await res.json();
        window.location.href = data.redirect_url;
        return;
    }

    const input = document.getElementById('answer-input');
    const answer = input.value.trim();
    if (!answer) return;

    const res = await fetch('/grammar/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({answer})
    });
    const data = await res.json();
    answered = true;

    const feedback = document.getElementById('feedback');
    feedback.classList.remove('hidden');
    input.disabled = true;

    if (data.correct) {
        input.classList.add('correct-input');
        feedback.textContent = 'Correct! 🎉';
        feedback.className = 'text-center font-semibold mb-4 text-green-400';
    } else {
        input.classList.add('wrong-input');
        feedback.textContent = `Not quite — the answer was "${data.correct_answer}"`;
        feedback.className = 'text-center font-semibold mb-4 text-red-400';
    }

    // Switch button to "Next" state using inline styles so theme overrides can't interfere
    const btn = document.getElementById('action-btn');
    btn.textContent = 'Next →';
    btn.style.backgroundColor = '#3d3d3d';
    btn.style.color = '#f0ebe3';
}

// Keyboard shortcut: Enter submits or advances
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') handleSubmit();
});

// Focus input on load
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('answer-input').focus();
});
