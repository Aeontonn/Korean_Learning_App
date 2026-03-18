"""
User statistics and progress tracking with data persistence
"""
import json
import os

class UserStats:
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.streak = 0
        self.words_mastered = set()
        self.difficult_words = {}  # word: times_wrong
        
        self.data_file = "user_data.json"
        self.load_stats()
    
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
                    # Convert list back to set
                    self.words_mastered = set(data.get("words_mastered", []))
            except Exception as e:
                print(f"Error loading data: {e}")
                # If error, start fresh
    
    def save_stats(self):
        """Save current stats to local file"""
        data = {
            "correct": self.correct,
            "incorrect": self.incorrect,
            "streak": self.streak,
            "difficult_words": self.difficult_words,
            "words_mastered": list(self.words_mastered) # Sets aren't JSON serializable
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def mark_correct(self, word_korean=None):
        """Record a correct answer"""
        self.correct += 1
        self.streak += 1
        
        # If they get a difficult word right, remove it from the difficult list
        if word_korean and word_korean in self.difficult_words:
            del self.difficult_words[word_korean]
            
        self.save_stats() # Save immediately

    def mark_incorrect(self, word_korean=None):
        """Record an incorrect answer"""
        self.incorrect += 1
        self.streak = 0
        
        if word_korean:
            if word_korean in self.difficult_words:
                self.difficult_words[word_korean] += 1
            else:
                self.difficult_words[word_korean] = 1
        
        self.save_stats() # Save immediately

    def mark_mastered(self, word_korean):
        """Mark a word as mastered"""
        self.words_mastered.add(word_korean)
        if word_korean in self.difficult_words:
            del self.difficult_words[word_korean]
        self.save_stats() # Save immediately

    def get_difficult_words(self):
        """Get list of difficult words sorted by frequency"""
        return sorted(self.difficult_words.items(), key=lambda x: x[1], reverse=True)