from datetime import date, timedelta
from flask import Blueprint, render_template, current_app, jsonify

home_bp = Blueprint("home", __name__)

def build_calendar(practice_dates, weeks=14):
    """Build a weeks x 7 grid of days for the streak calendar.
    Each cell: {date, practiced, is_future, is_today, label}
    Starts on a Monday, going back `weeks` weeks from today."""
    today = date.today()
    # Roll back to the most recent Monday
    start = today - timedelta(days=today.weekday(), weeks=weeks - 1)
    grid = []
    for w in range(weeks):
        week = []
        for d in range(7):
            day = start + timedelta(weeks=w, days=d)
            week.append({
                "date": day.isoformat(),
                "practiced": day.isoformat() in practice_dates,
                "is_future": day > today,
                "is_today": day == today,
                "label": day.strftime("%b %d"),
            })
        grid.append(week)
    return grid

@home_bp.route("/")
def index():
    stats = current_app.user_stats
    mastered_count = len(stats.words_mastered)
    due_count = len(stats.get_due_words())
    all_words = current_app.vocab_data.get_all_words()
    word_of_day = all_words[date.today().toordinal() % len(all_words)] if all_words else None
    calendar = build_calendar(stats.practice_dates)
    return render_template("home.html",
        correct=stats.correct,
        incorrect=stats.incorrect,
        streak=stats.streak,
        mastered_count=mastered_count,
        due_count=due_count,
        word_of_day=word_of_day,
        calendar=calendar,
    )

@home_bp.route("/api/stats")
def api_stats():
    stats = current_app.user_stats
    return jsonify(
        correct=stats.correct,
        incorrect=stats.incorrect,
        streak=stats.streak,
        mastered_count=len(stats.words_mastered),
        due_count=len(stats.get_due_words())
    )
