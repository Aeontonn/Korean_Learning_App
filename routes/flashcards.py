import random
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app

flashcards_bp = Blueprint("flashcards", __name__)

def get_categories(words):
    """Return sorted list of unique categories from a word pool."""
    return sorted({w["category"] for w in words if w.get("category")})

@flashcards_bp.route("/")
def setup():
    all_words = current_app.vocab_data.get_all_words()
    categories = get_categories(all_words)
    return render_template("flashcards/setup.html", categories=categories)

@flashcards_bp.route("/start", methods=["POST"])
def start():
    difficulty = request.form.get("difficulty", "basic")
    category = request.form.get("category", "all")
    words = current_app.vocab_data.get_words_cumulative(difficulty)
    if category and category != "all":
        filtered = [w for w in words if w.get("category") == category]
        words = filtered if filtered else words
    # Filter mastered
    mastered = current_app.user_stats.words_mastered
    words = [w for w in words if w["korean"] not in mastered] or words
    random.shuffle(words)
    # Store only keys in session to keep cookie small
    session["fc_keys"] = [w["korean"] for w in words]
    session["fc_index"] = 0
    session["fc_difficulty"] = difficulty
    return redirect(url_for("flashcards.session_view"))

@flashcards_bp.route("/session")
def session_view():
    keys = session.get("fc_keys", [])
    index = session.get("fc_index", 0)
    if not keys:
        return redirect(url_for("flashcards.setup"))
    all_words = {w["korean"]: w for w in current_app.vocab_data.get_all_words()}
    word = all_words.get(keys[index], {})
    return render_template("flashcards/session.html",
        word=word,
        index=index,
        total=len(keys)
    )

@flashcards_bp.route("/navigate", methods=["POST"])
def navigate():
    direction = request.json.get("direction", "next")
    keys = session.get("fc_keys", [])
    index = session.get("fc_index", 0)
    if direction == "next" and index < len(keys) - 1:
        index += 1
    elif direction == "prev" and index > 0:
        index -= 1
    session["fc_index"] = index
    all_words = {w["korean"]: w for w in current_app.vocab_data.get_all_words()}
    word = all_words.get(keys[index], {})
    return jsonify(
        korean=word.get("korean", ""),
        english=word.get("english", ""),
        index=index,
        total=len(keys),
        is_last=(index == len(keys) - 1)
    )
