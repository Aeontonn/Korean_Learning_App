"""
Tests for data/grammar.py – GrammarData unit tests.
"""
import pytest

from data.grammar import GrammarData

REQUIRED_KEYS = {"explanation", "example", "answer", "translation", "difficulty"}
DIFFICULTY_LEVELS = ("basic", "intermediate", "advanced")


@pytest.fixture(scope="module")
def grammar():
    return GrammarData()


# ---------------------------------------------------------------------------
# get_all_patterns
# ---------------------------------------------------------------------------

def test_get_all_patterns_returns_all(grammar):
    all_patterns = grammar.get_all_patterns()
    assert len(all_patterns) > 0
    # The full list must equal the raw internal list
    assert all_patterns is grammar.patterns


# ---------------------------------------------------------------------------
# get_patterns_by_difficulty (cumulative)
# ---------------------------------------------------------------------------

def test_get_patterns_basic_returns_only_basic(grammar):
    patterns = grammar.get_patterns_by_difficulty("basic")
    for p in patterns:
        assert p["difficulty"] == "basic"


def test_get_patterns_intermediate_includes_basic(grammar):
    patterns = grammar.get_patterns_by_difficulty("intermediate")
    difficulties = {p["difficulty"] for p in patterns}
    # Must contain both basic and intermediate
    assert "basic" in difficulties
    assert "intermediate" in difficulties
    # Must NOT contain advanced
    assert "advanced" not in difficulties


def test_get_patterns_advanced_returns_all(grammar):
    advanced_patterns = grammar.get_patterns_by_difficulty("advanced")
    all_patterns = grammar.get_all_patterns()
    assert len(advanced_patterns) == len(all_patterns)


# ---------------------------------------------------------------------------
# Data-quality checks
# ---------------------------------------------------------------------------

def test_all_patterns_have_required_keys(grammar):
    for pattern in grammar.get_all_patterns():
        missing = REQUIRED_KEYS - pattern.keys()
        assert not missing, f"Pattern missing keys {missing}: {pattern}"
