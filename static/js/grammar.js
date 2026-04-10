let answered = false;

async function handleSubmit() {
    if (answered) {
        // In "next" mode — go to next question
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

    const btn = document.getElementById('action-btn');
    btn.textContent = 'Next →';
    btn.classList.replace('bg-indigo-600', 'bg-slate-600');
    btn.classList.replace('hover:bg-indigo-500', 'hover:bg-slate-500');
}

// Focus input on load
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('answer-input').focus();
});
