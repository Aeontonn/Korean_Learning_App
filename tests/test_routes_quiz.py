"""
Tests for routes/quiz.py.
"""
import json


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _start_quiz(client, difficulty="basic"):
    """POST to /quiz/start and return the response without following redirects."""
    return client.post(
        "/quiz/start",
        data={"difficulty": difficulty},
        follow_redirects=False,
    )


def _setup_quiz_session(client, difficulty="basic"):
    """
    Drive the client through /quiz/start so that a quiz session exists,
    then return to the question page.
    """
    client.post("/quiz/start", data={"difficulty": difficulty}, follow_redirects=True)


def _get_correct_answer(client, app):
    """Read the current quiz question from session and return its correct English answer."""
    with client.session_transaction() as sess:
        keys = sess.get("quiz_keys", [])
        index = sess.get("quiz_index", 0)
    if not keys:
        return None
    korean = keys[index]
    all_words = {w["korean"]: w for w in app.vocab_data.get_all_words()}
    return all_words.get(korean, {}).get("english", "")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_quiz_setup_returns_200(client):
    response = client.get("/quiz/")
    assert response.status_code == 200


def test_quiz_start_redirects_to_question(client):
    response = _start_quiz(client)
    assert response.status_code == 302
    assert "/quiz/question" in response.headers["Location"]


def test_quiz_question_returns_200_after_start(client):
    _setup_quiz_session(client)
    response = client.get("/quiz/question")
    assert response.status_code == 200


def test_quiz_answer_correct(client, app):
    _setup_quiz_session(client)
    correct_answer = _get_correct_answer(client, app)
    assert correct_answer is not None

    response = client.post("/quiz/answer", json={"answer": correct_answer})
    assert response.status_code == 200

    data = response.get_json()
    assert data["correct"] is True
    assert data["score"] >= 1


def test_quiz_answer_incorrect(client, app):
    _setup_quiz_session(client)
    correct_answer = _get_correct_answer(client, app)

    # Deliberately send a wrong answer that can't match the correct one
    wrong_answer = "__intentionally_wrong__"
    assert wrong_answer != correct_answer

    response = client.post("/quiz/answer", json={"answer": wrong_answer})
    assert response.status_code == 200

    data = response.get_json()
    assert data["correct"] is False


def test_quiz_next_advances_index(client):
    _setup_quiz_session(client)

    with client.session_transaction() as sess:
        index_before = sess.get("quiz_index", 0)

    client.post("/quiz/next")

    with client.session_transaction() as sess:
        index_after = sess.get("quiz_index", 0)

    assert index_after == index_before + 1


def test_quiz_results_returns_200(client):
    _setup_quiz_session(client)
    # Advance index past the end so the results page is shown
    with client.session_transaction() as sess:
        sess["quiz_index"] = len(sess.get("quiz_keys", [])) + 1

    response = client.get("/quiz/results")
    assert response.status_code == 200
