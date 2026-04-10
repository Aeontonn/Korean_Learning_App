import random
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app

grammar_bp = Blueprint("grammar", __name__)

@grammar_bp.route("/")
def setup():
    return render_template("grammar/setup.html")

@grammar_bp.route("/start", methods=["POST"])
def start():
    difficulty = request.form.get("difficulty", "basic")
    patterns = current_app.grammar_data.get_patterns_by_difficulty(difficulty).copy()
    random.shuffle(patterns)
    session["gram_patterns"] = patterns
    session["gram_index"] = 0
    session["gram_score"] = 0
    return redirect(url_for("grammar.question"))

@grammar_bp.route("/question")
def question():
    patterns = session.get("gram_patterns", [])
    index = session.get("gram_index", 0)
    score = session.get("gram_score", 0)
    if not patterns:
        return redirect(url_for("grammar.setup"))
    if index >= len(patterns):
        return redirect(url_for("grammar.results"))
    pattern = patterns[index]
    return render_template("grammar/question.html",
        pattern=pattern,
        index=index,
        total=len(patterns),
        score=score
    )

@grammar_bp.route("/answer", methods=["POST"])
def answer():
    data = request.json
    user_answer = " ".join(data.get("answer", "").split())
    patterns = session.get("gram_patterns", [])
    index = session.get("gram_index", 0)
    pattern = patterns[index] if index < len(patterns) else {}
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
        total=len(patterns)
    )

@grammar_bp.route("/next", methods=["POST"])
def next_question():
    session["gram_index"] = session.get("gram_index", 0) + 1
    index = session["gram_index"]
    total = len(session.get("gram_patterns", []))
    if index >= total:
        return jsonify(done=True, redirect_url=url_for("grammar.results"))
    return jsonify(done=False, redirect_url=url_for("grammar.question"))

@grammar_bp.route("/results")
def results():
    score = session.get("gram_score", 0)
    total = len(session.get("gram_patterns", []))
    percentage = round((score / total * 100) if total > 0 else 0)
    return render_template("grammar/results.html", score=score, total=total, percentage=percentage)
