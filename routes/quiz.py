import random
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app

quiz_bp = Blueprint("quiz", __name__)
MAX_QUIZ_QUESTIONS = 50

@quiz_bp.route("/")
def setup():
    return render_template("quiz/setup.html")

@quiz_bp.route("/start", methods=["POST"])
def start():
    difficulty = request.form.get("difficulty", "basic")
    word_pool = current_app.vocab_data.get_words_cumulative(difficulty)
    mastered = current_app.user_stats.words_mastered
    unmastered = [w for w in word_pool if w["korean"] not in mastered]
    words = (unmastered if unmastered else word_pool).copy()
    random.shuffle(words)
    words = words[:MAX_QUIZ_QUESTIONS]
    session["quiz_keys"] = [w["korean"] for w in words]
    session["quiz_pool_keys"] = [w["korean"] for w in word_pool]
    session["quiz_index"] = 0
    session["quiz_score"] = 0
    session["quiz_difficulty"] = difficulty
    session["quiz_source"] = "normal"
    return redirect(url_for("quiz.question"))

@quiz_bp.route("/question")
def question():
    keys = session.get("quiz_keys", [])
    index = session.get("quiz_index", 0)
    score = session.get("quiz_score", 0)
    if not keys:
        return redirect(url_for("quiz.setup"))
    if index >= len(keys):
        return redirect(url_for("quiz.results"))
    all_words = {w["korean"]: w for w in current_app.vocab_data.get_all_words()}
    pool_keys = session.get("quiz_pool_keys", keys)
    current_word = all_words.get(keys[index], {})
    correct_answer = current_word.get("english", "")
    wrong_pool = [all_words[k]["english"] for k in pool_keys if all_words.get(k, {}).get("english") != correct_answer]
    wrong = random.sample(wrong_pool, min(3, len(wrong_pool)))
    choices = [correct_answer] + wrong
    random.shuffle(choices)
    return render_template("quiz/question.html",
        word=current_word,
        choices=choices,
        index=index,
        total=len(keys),
        score=score
    )

@quiz_bp.route("/answer", methods=["POST"])
def answer():
    data = request.json
    selected = data.get("answer", "")
    keys = session.get("quiz_keys", [])
    index = session.get("quiz_index", 0)
    all_words = {w["korean"]: w for w in current_app.vocab_data.get_all_words()}
    current_word = all_words.get(keys[index], {})
    correct_answer = current_word.get("english", "")
    is_correct = selected == correct_answer
    if is_correct:
        session["quiz_score"] = session.get("quiz_score", 0) + 1
        current_app.user_stats.mark_correct(current_word.get("korean"))
    else:
        current_app.user_stats.mark_incorrect(current_word.get("korean"))
    return jsonify(
        correct=is_correct,
        correct_answer=correct_answer,
        score=session["quiz_score"],
        total=len(keys)
    )

@quiz_bp.route("/next", methods=["POST"])
def next_question():
    session["quiz_index"] = session.get("quiz_index", 0) + 1
    index = session["quiz_index"]
    total = len(session.get("quiz_keys", []))
    if index >= total:
        return jsonify(done=True, redirect_url=url_for("quiz.results"))
    return jsonify(done=False, redirect_url=url_for("quiz.question"))

@quiz_bp.route("/results")
def results():
    score = session.get("quiz_score", 0)
    total = len(session.get("quiz_keys", []))
    percentage = round((score / total * 100) if total > 0 else 0)
    return render_template("quiz/results.html", score=score, total=total, percentage=percentage)
