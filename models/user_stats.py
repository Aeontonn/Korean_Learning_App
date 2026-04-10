"""
User statistics and progress tracking with data persistence.
Includes spaced repetition (SRS) and auto-mastery logic.
"""
import json
import os
from datetime import date

# How many consecutive correct answers before a word is auto-mastered
MASTERY_THRESHOLD = 4

# SRS interval bounds (days)
SRS_MIN_INTERVAL = 1
SRS_MAX_INTERVAL = 30


class UserStats:
    def __init__(self):
        self._reset_stats()

        # Absolute path so the file is always found regardless of where the app is launched from
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_data.json")
        self.load_stats()

    def _reset_stats(self):
        """Reset all stats to defaults (used on load failure or first run)"""
        self.correct = 0
        self.incorrect = 0
        self.streak = 0
        self.words_mastered = set()
        self.difficult_words = {}       # word -> total times wrong
        self.word_correct_streak = {}   # word -> consecutive correct count (for auto-mastery)
        self.word_last_seen = {}        # word -> "YYYY-MM-DD" (for SRS)
        self.word_intervals = {}        # word -> days until next review (for SRS)

    def load_stats(self):
        """Load stats from local file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.correct = data.get("correct", 0)
                    self.incorrect = data.get("incorrect", 0)
                    self.streak = data.get("streak", 0)
                    self.difficult_words = data.get("difficult_words", {})
                    self.words_mastered = set(data.get("words_mastered", []))
                    self.word_correct_streak = data.get("word_correct_streak", {})
                    self.word_last_seen = data.get("word_last_seen", {})
                    self.word_intervals = data.get("word_intervals", {})
            except json.JSONDecodeError:
                print("Warning: user_data.json is corrupted. Starting with fresh stats.")
                self._reset_stats()
            except Exception as e:
                print(f"Error loading data: {e}. Starting with fresh stats.")
                self._reset_stats()

    def save_stats(self):
        """Save current stats to local file"""
        data = {
            "correct": self.correct,
            "incorrect": self.incorrect,
            "streak": self.streak,
            "difficult_words": self.difficult_words,
            "words_mastered": list(self.words_mastered),
            "word_correct_streak": self.word_correct_streak,
            "word_last_seen": self.word_last_seen,
            "word_intervals": self.word_intervals,
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def mark_correct(self, word_korean=None):
        """Record a correct answer. Handles auto-mastery and SRS scheduling."""
        self.correct += 1
        self.streak += 1

        if word_korean:
            # Clear from difficult list — they got it right
            if word_korean in self.difficult_words:
                del self.difficult_words[word_korean]

            # Auto-mastery: track consecutive correct streak
            self.word_correct_streak[word_korean] = self.word_correct_streak.get(word_korean, 0) + 1
            if self.word_correct_streak[word_korean] >= MASTERY_THRESHOLD:
                self.mark_mastered(word_korean)
                return  # mark_mastered calls save_stats already

            # SRS: double the review interval on correct (cap at SRS_MAX_INTERVAL days)
            today = date.today().isoformat()
            self.word_last_seen[word_korean] = today
            current_interval = self.word_intervals.get(word_korean, SRS_MIN_INTERVAL)
            self.word_intervals[word_korean] = min(current_interval * 2, SRS_MAX_INTERVAL)

        self.save_stats()

    def mark_incorrect(self, word_korean=None):
        """Record an incorrect answer. Resets streak and SRS interval."""
        self.incorrect += 1
        self.streak = 0

        if word_korean:
            # Add to difficult words
            self.difficult_words[word_korean] = self.difficult_words.get(word_korean, 0) + 1

            # Reset consecutive correct streak
            self.word_correct_streak[word_korean] = 0

            # SRS: reset interval to 1 day so it comes back soon
            today = date.today().isoformat()
            self.word_last_seen[word_korean] = today
            self.word_intervals[word_korean] = SRS_MIN_INTERVAL

        self.save_stats()

    def mark_mastered(self, word_korean):
        """Mark a word as fully mastered — removes it from all review queues."""
        self.words_mastered.add(word_korean)
        self.difficult_words.pop(word_korean, None)
        self.word_correct_streak.pop(word_korean, None)
        self.word_last_seen.pop(word_korean, None)
        self.word_intervals.pop(word_korean, None)
        self.save_stats()

    def get_difficult_words(self):
        """Get list of difficult words sorted by error count (most errors first)"""
        return sorted(self.difficult_words.items(), key=lambda x: x[1], reverse=True)

    def get_due_words(self):
        """Return words due for SRS review today, sorted by most overdue first."""
        today = date.today()
        due = []
        for word, last_seen_str in self.word_last_seen.items():
            if word in self.words_mastered:
                continue
            last_seen = date.fromisoformat(last_seen_str)
            interval = self.word_intervals.get(word, SRS_MIN_INTERVAL)
            days_overdue = (today - last_seen).days - interval
            if days_overdue >= 0:
                due.append({"korean": word, "days_overdue": days_overdue})
        return sorted(due, key=lambda x: x["days_overdue"], reverse=True)
