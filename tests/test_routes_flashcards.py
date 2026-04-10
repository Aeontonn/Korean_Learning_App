"""
Tests for routes/flashcards.py.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _start_flashcards(client, difficulty="basic"):
    """POST to /flashcards/start and return the response."""
    return client.post(
        "/flashcards/start",
        data={"difficulty": difficulty},
        follow_redirects=False,
    )


def _setup_flashcard_session(client, difficulty="basic"):
    """Drive the client through /flashcards/start, following redirects."""
    client.post("/flashcards/start", data={"difficulty": difficulty}, follow_redirects=True)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_flashcard_setup_returns_200(client):
    response = client.get("/flashcards/")
    assert response.status_code == 200


def test_flashcard_start_redirects(client):
    response = _start_flashcards(client)
    assert response.status_code == 302
    assert "/flashcards/session" in response.headers["Location"]


def test_flashcard_session_returns_200_after_start(client):
    _setup_flashcard_session(client)
    response = client.get("/flashcards/session")
    assert response.status_code == 200


def test_flashcard_navigate_next(client):
    _setup_flashcard_session(client)

    with client.session_transaction() as sess:
        index_before = sess.get("fc_index", 0)

    response = client.post("/flashcards/navigate", json={"direction": "next"})
    assert response.status_code == 200

    data = response.get_json()
    # index should have advanced (assuming more than one card)
    assert data["index"] == index_before + 1


def test_flashcard_navigate_prev_at_start_stays(client):
    """Navigating prev from index 0 should stay at index 0."""
    _setup_flashcard_session(client)

    # Ensure we're at the start
    with client.session_transaction() as sess:
        sess["fc_index"] = 0

    response = client.post("/flashcards/navigate", json={"direction": "prev"})
    assert response.status_code == 200

    data = response.get_json()
    assert data["index"] == 0
