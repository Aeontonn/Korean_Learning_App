// Keyboard shortcuts: 1/2/3/4 select answer, Enter advances to next question
document.addEventListener('keydown', function(e) {
    const num = parseInt(e.key);
    if (num >= 1 && num <= 4) {
        const btns = document.querySelectorAll('.btn-choice:not(:disabled)');
        if (btns[num - 1]) btns[num - 1].click();
    }
    if (e.key === 'Enter') {
        const nextBtn = document.getElementById('next-btn');
        if (nextBtn && !nextBtn.classList.contains('hidden')) nextBtn.click();
    }
});

async function submitAnswer(btn, choice) {
    // Disable all buttons immediately
    document.querySelectorAll('.btn-choice').forEach(b => b.disabled = true);

    const res = await fetch('/quiz/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({answer: choice})
    });
    const data = await res.json();

    // Colour the buttons
    document.querySelectorAll('.btn-choice').forEach(b => {
        if (b.dataset.choice === data.correct_answer) b.classList.add('reveal');
    });
    if (!data.correct) {
        btn.classList.add('wrong');
    }

    // Show feedback
    const feedback = document.getElementById('feedback');
    feedback.classList.remove('hidden');
    if (data.correct) {
        feedback.textContent = 'Correct! 🎉';
        feedback.className = 'text-center font-semibold text-lg mb-4 text-green-400';
    } else {
        feedback.textContent = `Not quite — the answer was "${data.correct_answer}"`;
        feedback.className = 'text-center font-semibold text-lg mb-4 text-red-400';
    }

    // Update score
    document.getElementById('score-display').textContent = `Score: ${data.score} / ${data.total}`;

    // Show next button
    document.getElementById('next-btn').classList.remove('hidden');
}

async function goNext() {
    const res = await fetch('/quiz/next', {method: 'POST'});
    const data = await res.json();
    window.location.href = data.redirect_url;
}
