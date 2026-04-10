import random
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app

grammar_bp = Blueprint("grammar", __name__)

@grammar_bp.route("/")
def setup():
    return render_template("grammar/setup.html")

def _get_all_patterns():
    """Return the full ordered pattern list from the app."""
    from flask import current_app
    return current_app.grammar_data.get_all_patterns()

def _lookup_pattern(order, pos):
    """Get the pattern at position pos in the shuffled order list."""
    all_patterns = _get_all_patterns()
    if pos < len(order):
        return all_patterns[order[pos]]
    return {}

@grammar_bp.route("/start", methods=["POST"])
def start():
    difficulty = request.form.get("difficulty", "basic")
    all_patterns = current_app.grammar_data.get_all_patterns()
    filtered = current_app.grammar_data.get_patterns_by_difficulty(difficulty)

    # Store only the indices of matching patterns — keeps the cookie tiny
    indices = [i for i, p in enumerate(all_patterns) if p in filtered]
    random.shuffle(indices)

    session["gram_order"] = indices          # shuffled indices into the master list
    session["gram_difficulty"] = difficulty
    session["gram_index"] = 0
    session["gram_score"] = 0
    session["gram_total"] = len(indices)
    return redirect(url_for("grammar.question"))

@grammar_bp.route("/question")
def question():
    order = session.get("gram_order", [])
    index = session.get("gram_index", 0)
    score = session.get("gram_score", 0)
    total = session.get("gram_total", 0)

    if not order:
        return redirect(url_for("grammar.setup"))
    if index >= total:
        return redirect(url_for("grammar.results"))

    pattern = _lookup_pattern(order, index)
    return render_template("grammar/question.html",
        pattern=pattern,
        index=index,
        total=total,
        score=score,
        difficulty=session.get("gram_difficulty", "basic")
    )

@grammar_bp.route("/answer", methods=["POST"])
def answer():
    data = request.json
    user_answer = " ".join(data.get("answer", "").split())
    order = session.get("gram_order", [])
    index = session.get("gram_index", 0)
    total = session.get("gram_total", 0)

    pattern = _lookup_pattern(order, index)
    correct_answer = " ".join(pattern.get("answer", "").split())
    is_correct = user_answer == correct_answer

    if is_correct:
        session["gram_score"] = session.get("gram_score", 0) + 1
        current_app.user_stats.mark_correct()
    else:
        current_app.user_stats.mark_incorrect()

    return jsonify(
        correct=is_correct,
        correct_answer=pattern.get("answer", ""),
        score=session["gram_score"],
        total=total
    )

@grammar_bp.route("/next", methods=["POST"])
def next_question():
    session["gram_index"] = session.get("gram_index", 0) + 1
    index = session["gram_index"]
    total = session.get("gram_total", 0)
    if index >= total:
        return jsonify(done=True, redirect_url=url_for("grammar.results"))
    return jsonify(done=False, redirect_url=url_for("grammar.question"))

@grammar_bp.route("/results")
def results():
    score = session.get("gram_score", 0)
    total = session.get("gram_total", 0)
    percentage = round((score / total * 100) if total > 0 else 0)
    difficulty = session.get("gram_difficulty", "basic")
    return render_template("grammar/results.html",
        score=score, total=total, percentage=percentage, difficulty=difficulty)
