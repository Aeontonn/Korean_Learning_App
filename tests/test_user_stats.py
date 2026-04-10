"""
Tests for models/user_stats.py – UserStats unit tests.
"""
import json
from datetime import date, timedelta

import pytest

from models.user_stats import UserStats, MASTERY_THRESHOLD, SRS_MIN_INTERVAL, SRS_MAX_INTERVAL

WORD = "안녕하세요"
WORD2 = "감사합니다"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_stats(tmp_path, filename="user_data.json"):
    """Return a fresh UserStats instance backed by a temp file."""
    stats = UserStats.__new__(UserStats)
    stats._reset_stats()
    stats.data_file = str(tmp_path / filename)
    return stats


# ---------------------------------------------------------------------------
# Basic correct / incorrect counters
# ---------------------------------------------------------------------------

def test_mark_correct_increments_correct_count(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_correct(WORD)
    assert stats.correct == 1


def test_mark_incorrect_increments_incorrect_count(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_incorrect(WORD)
    assert stats.incorrect == 1


# ---------------------------------------------------------------------------
# Streak behaviour
# ---------------------------------------------------------------------------

def test_streak_resets_on_incorrect(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_correct(WORD)
    stats.mark_correct(WORD2)
    assert stats.streak == 2
    stats.mark_incorrect(WORD)
    assert stats.streak == 0


def test_streak_increments_on_correct(tmp_path):
    stats = _make_stats(tmp_path)
    for _ in range(3):
        stats.mark_correct(WORD2)
    # streak resets after auto-mastery at MASTERY_THRESHOLD=4; 3 is safe
    assert stats.streak == 3


# ---------------------------------------------------------------------------
# Difficult words list
# ---------------------------------------------------------------------------

def test_difficult_word_added_on_incorrect(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_incorrect(WORD)
    assert WORD in stats.difficult_words
    assert stats.difficult_words[WORD] == 1


def test_difficult_word_removed_on_correct(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_incorrect(WORD)
    assert WORD in stats.difficult_words
    stats.mark_correct(WORD)
    assert WORD not in stats.difficult_words


# ---------------------------------------------------------------------------
# Auto-mastery
# ---------------------------------------------------------------------------

def test_auto_mastery_after_threshold(tmp_path):
    """MASTERY_THRESHOLD consecutive correct answers on the same word auto-masters it."""
    stats = _make_stats(tmp_path)
    for _ in range(MASTERY_THRESHOLD):
        stats.mark_correct(WORD)
    assert WORD in stats.words_mastered


def test_mastered_word_removed_from_difficult(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_incorrect(WORD)
    assert WORD in stats.difficult_words
    # Drive it to mastery
    for _ in range(MASTERY_THRESHOLD):
        stats.mark_correct(WORD)
    assert WORD in stats.words_mastered
    assert WORD not in stats.difficult_words


# ---------------------------------------------------------------------------
# SRS interval
# ---------------------------------------------------------------------------

def test_srs_interval_doubles_on_correct(tmp_path):
    stats = _make_stats(tmp_path)
    # First correct answer: interval starts at SRS_MIN_INTERVAL (1), then doubles to 2
    stats.mark_correct(WORD)
    assert stats.word_intervals[WORD] == SRS_MIN_INTERVAL * 2


def test_srs_interval_resets_on_incorrect(tmp_path):
    stats = _make_stats(tmp_path)
    # Build up a larger interval first
    stats.mark_correct(WORD)
    stats.mark_correct(WORD)
    assert stats.word_intervals[WORD] > SRS_MIN_INTERVAL
    # Now mark incorrect → should reset to SRS_MIN_INTERVAL
    stats.mark_incorrect(WORD)
    assert stats.word_intervals[WORD] == SRS_MIN_INTERVAL


# ---------------------------------------------------------------------------
# get_due_words
# ---------------------------------------------------------------------------

def test_get_due_words_returns_overdue(tmp_path):
    stats = _make_stats(tmp_path)
    ten_days_ago = (date.today() - timedelta(days=10)).isoformat()
    stats.word_last_seen[WORD] = ten_days_ago
    stats.word_intervals[WORD] = 1   # interval = 1 day → overdue by 9 days

    due = stats.get_due_words()
    due_words = [entry["korean"] for entry in due]
    assert WORD in due_words


def test_get_due_words_excludes_mastered(tmp_path):
    stats = _make_stats(tmp_path)
    ten_days_ago = (date.today() - timedelta(days=10)).isoformat()
    stats.word_last_seen[WORD] = ten_days_ago
    stats.word_intervals[WORD] = 1
    stats.words_mastered.add(WORD)

    due = stats.get_due_words()
    due_words = [entry["korean"] for entry in due]
    assert WORD not in due_words


# ---------------------------------------------------------------------------
# Persistence – save / load roundtrip
# ---------------------------------------------------------------------------

def test_save_and_load_roundtrip(tmp_path):
    stats = _make_stats(tmp_path)
    stats.mark_correct(WORD)
    stats.mark_incorrect(WORD2)
    stats.words_mastered.add("마시다")

    original_correct = stats.correct
    original_incorrect = stats.incorrect
    original_streak = stats.streak
    original_mastered = set(stats.words_mastered)
    original_difficult = dict(stats.difficult_words)

    stats.save_stats()

    # Load into a fresh instance pointing at the same file
    stats2 = UserStats.__new__(UserStats)
    stats2._reset_stats()
    stats2.data_file = stats.data_file
    stats2.load_stats()

    assert stats2.correct == original_correct
    assert stats2.incorrect == original_incorrect
    assert stats2.streak == original_streak
    assert stats2.words_mastered == original_mastered
    assert stats2.difficult_words == original_difficult


def test_corrupt_json_resets_gracefully(tmp_path):
    data_file = tmp_path / "user_data.json"
    data_file.write_text("THIS IS NOT JSON {{{", encoding="utf-8")

    stats = UserStats.__new__(UserStats)
    stats._reset_stats()
    stats.data_file = str(data_file)
    stats.load_stats()   # must not raise

    # All fields should be at defaults after corrupt-load recovery
    assert stats.correct == 0
    assert stats.incorrect == 0
    assert stats.streak == 0
    assert stats.words_mastered == set()
    assert stats.difficult_words == {}
