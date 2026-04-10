"""
Root conftest.py – shared pytest fixtures for the Korean learning app.
"""
import json
import pytest

from flask_app import create_app
from models.user_stats import UserStats


@pytest.fixture()
def app(tmp_path):
    """
    Create a Flask application configured for testing.

    UserStats is replaced with a fresh instance that points to a temporary
    JSON file so tests never touch the real user_data.json on disk.
    """
    flask_app = create_app()
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
    )

    # Wire up a fresh UserStats backed by a temp file
    tmp_data_file = str(tmp_path / "test_user_data.json")
    stats = UserStats.__new__(UserStats)   # skip __init__ (which auto-loads real file)
    stats._reset_stats()
    stats.data_file = tmp_data_file
    flask_app.user_stats = stats

    yield flask_app


@pytest.fixture()
def client(app):
    """A test client for the Flask app."""
    return app.test_client()


@pytest.fixture()
def fresh_stats(tmp_path):
    """
    A UserStats instance backed by a fresh temp file.

    Use this in unit tests that exercise UserStats directly without
    going through the Flask app.
    """
    tmp_data_file = str(tmp_path / "user_data.json")
    stats = UserStats.__new__(UserStats)
    stats._reset_stats()
    stats.data_file = tmp_data_file
    return stats
