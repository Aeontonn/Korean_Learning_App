import random
from flask import Blueprint, render_template, redirect, url_for, session, current_app

review_bp = Blueprint("review", __name__)

@review_bp.route("/")
def index():
    stats = current_app.user_stats
    all_words = {w["korean"]: w for w in current_app.vocab_data.get_all_words()}

    difficult_list = stats.get_difficult_words()
    due_list = stats.get_due_words()

    review_words = []
    for korean, count in difficult_list:
        if korean in all_words:
            word = all_words[korean].copy()
            word["errors"] = count
            review_words.append(word)

    due_words = []
    for entry in due_list:
        korean = entry["korean"]
        if korean in all_words:
            word = all_words[korean].copy()
            word["days_overdue"] = entry["days_overdue"]
            due_words.append(word)

    if not review_words and not due_words:
        return render_template("review/empty.html")

    return render_template("review/list.html",
        review_words=review_words,
        due_words=due_words,
        total=len(review_words) + len(due_words)
    )

@review_bp.route("/start_practice", methods=["POST"])
def start_practice():
    stats = current_app.user_stats
    all_words = {w["korean"]: w for w in current_app.vocab_data.get_all_words()}

    difficult_list = stats.get_difficult_words()
    due_list = stats.get_due_words()

    seen = set()
    combined_keys = []
    for entry in due_list:
        k = entry["korean"]
        if k not in seen:
            seen.add(k)
            combined_keys.append(k)
    for korean, _ in difficult_list:
        if korean not in seen:
            seen.add(korean)
            combined_keys.append(korean)

    random.shuffle(combined_keys)
    session["quiz_keys"] = combined_keys
    session["quiz_pool_keys"] = [w["korean"] for w in current_app.vocab_data.get_all_words()]
    session["quiz_index"] = 0
    session["quiz_score"] = 0
    session["quiz_source"] = "review"
    return redirect(url_for("quiz.question"))
