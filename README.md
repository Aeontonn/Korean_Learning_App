# Korean Language Learning App

A desktop flashcard and quiz app for learning Korean vocabulary and grammar, built with Python and Tkinter.

## Requirements

- Python 3.8 or higher
- No third-party packages required — uses only the Python standard library (`tkinter` is included with Python)

## How to Run

```bash
python main.py
```

## Modes

### Flashcards

Browse Korean words one at a time. Click the card to flip between Korean and English. Use Previous / Next to navigate. Difficulty is cumulative — Intermediate shows Basic + Intermediate words, Advanced shows everything.

### Quiz

Multiple choice — pick the correct English meaning for a given Korean word. 4 options per question, up to 50 questions per session. Instant feedback with colour coding (green = correct, red = wrong). Tracks your score and feeds incorrect words into the Review queue automatically.

### Grammar Practice

Fill-in-the-blank exercises for Korean grammar particles and patterns. Difficulty-aware — Basic covers core particles (는/이/을/에), Intermediate adds comparisons and continuous tense, Advanced covers complex structures like `는 것 같아요` and `게 되었어요`.

### Review

Shows two queues:

- **Due for review (SRS)** — words scheduled for today based on your answer history
- **Missed in quizzes** — words you've gotten wrong, sorted by error count

Hit _Start Practice Quiz_ to drill them all in one session.

## Progress Tracking

All progress is saved automatically to `user_data.json` in the project root.

- **Streaks** — consecutive correct answers across all sessions
- **Difficult words** — words you miss are tracked and surfaced in Review mode
- **Auto-mastery** — get a word correct 3 times in a row and it's removed from future quizzes
- **Spaced repetition (SRS)** — correct answers push a word's next review date further out (interval doubles, up to 30 days). Wrong answers reset the interval to 1 day so the word comes back immediately

## Project Structure

```
├── main.py              # Entry point
├── app.py               # App controller and navigation
├── user_data.json       # Persisted user progress (auto-created)
├── data/
│   ├── vocabulary.py    # Korean word lists (basic / intermediate / advanced)
│   └── grammar.py       # Grammar pattern exercises
├── models/
│   └── user_stats.py    # Progress tracking, SRS logic, auto-mastery
└── gui/
    ├── main_menu.py     # Main menu
    ├── flashcards.py    # Flashcard mode
    ├── quiz.py          # Multiple choice quiz
    ├── grammar.py       # Grammar fill-in-the-blank
    └── review.py        # Review queue (SRS + difficult words)
```
