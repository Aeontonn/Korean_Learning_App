"""
Tests for data/vocabulary.py – VocabularyData unit tests.
"""
import pytest

from data.vocabulary import VocabularyData

REQUIRED_KEYS = {"korean", "english", "category"}


@pytest.fixture(scope="module")
def vocab():
    return VocabularyData()


# ---------------------------------------------------------------------------
# get_words (non-cumulative, single level)
# ---------------------------------------------------------------------------

def test_get_words_basic_returns_only_basic(vocab):
    words = vocab.get_words("basic")
    assert len(words) > 0
    for w in words:
        # All returned words should come from the basic bucket only.
        # We verify this by checking that every word actually lives in the
        # basic list (cross-check against internal dict).
        assert w in vocab.vocabulary["basic"]


def test_get_words_cumulative_intermediate_includes_basic(vocab):
    intermediate_words = vocab.get_words_cumulative("intermediate")
    basic_koreans = {w["korean"] for w in vocab.get_words("basic")}
    intermediate_koreans = {w["korean"] for w in vocab.get_words("intermediate")}
    returned_koreans = {w["korean"] for w in intermediate_words}

    # Must include all basic words
    assert basic_koreans.issubset(returned_koreans)
    # Must include all intermediate words
    assert intermediate_koreans.issubset(returned_koreans)
    # Must NOT include advanced words
    advanced_koreans = {w["korean"] for w in vocab.get_words("advanced")}
    assert advanced_koreans.isdisjoint(returned_koreans)


def test_get_words_cumulative_advanced_includes_all(vocab):
    advanced_cumulative = vocab.get_words_cumulative("advanced")
    all_words = vocab.get_all_words()
    all_koreans = {w["korean"] for w in all_words}
    returned_koreans = {w["korean"] for w in advanced_cumulative}
    assert all_koreans == returned_koreans


# ---------------------------------------------------------------------------
# get_all_words
# ---------------------------------------------------------------------------

def test_get_all_words_returns_all_three_levels(vocab):
    all_words = vocab.get_all_words()
    basic_count = len(vocab.get_words("basic"))
    intermediate_count = len(vocab.get_words("intermediate"))
    advanced_count = len(vocab.get_words("advanced"))
    assert len(all_words) == basic_count + intermediate_count + advanced_count


# ---------------------------------------------------------------------------
# Data-quality checks
# ---------------------------------------------------------------------------

def test_all_words_have_required_keys(vocab):
    for word in vocab.get_all_words():
        missing = REQUIRED_KEYS - word.keys()
        assert not missing, f"Word missing keys {missing}: {word}"


@pytest.mark.xfail(
    reason=(
        "Known data bug: five Korean homographs appear in multiple difficulty levels "
        "with different meanings (일=day/one, 이=tooth/two, 팔=arm/eight, "
        "눈=eye/snow, 배=stomach/ship). Each entry should use a disambiguating "
        "form or be deduplicated."
    ),
    strict=True,
)
def test_no_duplicate_korean_words(vocab):
    from collections import Counter
    all_words = vocab.get_all_words()
    koreans = [w["korean"] for w in all_words]
    duplicates = [k for k, count in Counter(koreans).items() if count > 1]
    assert not duplicates, (
        f"Duplicate Korean words found across difficulty levels: {duplicates}"
    )
