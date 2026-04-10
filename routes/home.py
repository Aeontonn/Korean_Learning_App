from flask import Blueprint, render_template, current_app, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    stats = current_app.user_stats
    mastered_count = len(stats.words_mastered)
    due_count = len(stats.get_due_words())
    return render_template("home.html",
        correct=stats.correct,
        incorrect=stats.incorrect,
        streak=stats.streak,
        mastered_count=mastered_count,
        due_count=due_count
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
