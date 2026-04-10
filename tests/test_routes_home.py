"""
Tests for routes/home.py – home page and stats API.
"""


def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_shows_stats(client, app):
    # Seed some known stats so we can confirm they appear in the page
    app.user_stats.correct = 7
    app.user_stats.incorrect = 3
    app.user_stats.streak = 2

    response = client.get("/")
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    # The page must render the seeded stats somewhere (as digits)
    assert "7" in html
    assert "3" in html
