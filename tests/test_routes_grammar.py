"""
Tests for routes/grammar.py.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _start_grammar(client, difficulty="basic"):
    return client.post(
        "/grammar/start",
        data={"difficulty": difficulty},
        follow_redirects=False,
    )


def _setup_grammar_session(client, difficulty="basic"):
    client.post("/grammar/start", data={"difficulty": difficulty}, follow_redirects=True)


def _get_correct_answer(client):
    """Return the correct answer for the current grammar question."""
    with client.session_transaction() as sess:
        patterns = sess.get("gram_patterns", [])
        index = sess.get("gram_index", 0)
    if not patterns or index >= len(patterns):
        return None
    return patterns[index].get("answer", "")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_grammar_setup_returns_200(client):
    response = client.get("/grammar/")
    assert response.status_code == 200


def test_grammar_start_redirects(client):
    response = _start_grammar(client)
    assert response.status_code == 302
    assert "/grammar/question" in response.headers["Location"]


def test_grammar_question_returns_200(client):
    _setup_grammar_session(client)
    response = client.get("/grammar/question")
    assert response.status_code == 200


def test_grammar_answer_correct(client):
    _setup_grammar_session(client)
    correct_answer = _get_correct_answer(client)
    assert correct_answer is not None

    response = client.post("/grammar/answer", json={"answer": correct_answer})
    assert response.status_code == 200

    data = response.get_json()
    assert data["correct"] is True
    assert data["score"] >= 1


def test_grammar_answer_incorrect(client):
    _setup_grammar_session(client)

    response = client.post("/grammar/answer", json={"answer": "__wrong__"})
    assert response.status_code == 200

    data = response.get_json()
    assert data["correct"] is False


def test_grammar_answer_normalises_whitespace(client):
    """An answer with leading/trailing or extra internal spaces should still pass."""
    _setup_grammar_session(client)
    correct_answer = _get_correct_answer(client)
    assert correct_answer is not None

    # Add extraneous whitespace around the correct answer
    padded = "  " + correct_answer + "  "

    response = client.post("/grammar/answer", json={"answer": padded})
    assert response.status_code == 200

    data = response.get_json()
    assert data["correct"] is True, (
        f"Expected normalised answer '{padded!r}' to match '{correct_answer!r}'"
    )
