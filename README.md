# Korean Language Learning App

A web app for learning Korean vocabulary and grammar, with spaced repetition, auto-mastery, and progress tracking.

**Live site:** [https://korean-learning-app-psxu.onrender.com](https://korean-learning-app-psxu.onrender.com)

---

## Tech Stack

- **Backend:** Python 3.8+, Flask 3.0
- **Frontend:** Jinja2 templates, Tailwind CSS, Vanilla JavaScript
- **Server:** Gunicorn
- **Hosting:** Render

---

## Modes

### Home Dashboard

Stats overview (correct/incorrect answers, streak, mastered words), a Word of the Day, a banner for SRS words due today, and a 14-week streak calendar.

### Flashcards

Browse Korean words one at a time. Click the card to flip between Korean and English. Filter by difficulty and category. Mastered words are excluded automatically.

### Quiz

Multiple choice — pick the correct English meaning for a given Korean word. 4 options per question, up to 50 questions per session. Instant colour-coded feedback (green = correct, red = wrong). Supports keyboard shortcuts (1–4 to select, Enter to advance). Incorrect answers are automatically added to the Review queue.

### Grammar Practice

Fill-in-the-blank exercises for Korean grammar particles and patterns. Difficulty-aware:

- **Basic** — core particles (은/는, 이/가, 을/를, 에, 에서)
- **Intermediate** — comparisons (보다), continuous tense (고 있어요), suggestions, permissions, causation
- **Advanced** — complex structures (는 것 같아요, 게 되었어요, 본 적이 있어요)

### Review

Two queues in one place:

- **Due for review (SRS)** — words scheduled for today based on answer history, sorted by most overdue
- **Missed in quizzes** — words you've gotten wrong, sorted by error count

Hit *Start Practice Quiz* to drill them all in one session.

---

## Progress Tracking

Progress is saved to `user_data.json`.

- **Streaks** — consecutive correct answers tracked across sessions
- **Difficult words** — missed words are surfaced in the Review queue
- **Auto-mastery** — get a word correct 4 times in a row and it's removed from future quizzes
- **Spaced repetition (SRS)** — correct answers push a word's next review date further out (interval doubles, up to 30 days). Wrong answers reset the interval to 1 day

---

## Running Locally

```bash
pip install -r requirements.txt
python flask_app.py
```

Then open [http://localhost:5000](http://localhost:5000).

---

## Project Structure

```
├── flask_app.py         # Flask app factory and entry point
├── requirements.txt     # flask, gunicorn
├── user_data.json       # Persisted user progress (auto-created)
├── data/
│   ├── vocabulary.py    # Korean word lists (basic / intermediate / advanced)
│   └── grammar.py       # Grammar pattern exercises
├── models/
│   └── user_stats.py    # Progress tracking, SRS logic, auto-mastery
├── routes/
│   ├── home.py          # Dashboard and stats API
│   ├── flashcards.py    # Flashcard session and navigation
│   ├── quiz.py          # Multiple choice quiz
│   ├── grammar.py       # Grammar fill-in-the-blank
│   └── review.py        # Review queue (SRS + difficult words)
├── templates/           # Jinja2 HTML templates
└── static/js/
    ├── quiz.js          # Keyboard shortcuts and answer feedback
    └── grammar.js       # Grammar input handling
```
