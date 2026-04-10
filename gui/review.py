import tkinter as tk
from tkinter import ttk, messagebox
import random
# We import QuizMode inside the method to avoid circular import issues

class ReviewMode:
    def __init__(self, root, app, difficulty):
        self.root = root
        self.app = app
        self.difficulty = difficulty
        
        self.clear_window()
        self.create_ui()
    
    def clear_window(self):
        """Remove all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_ui(self):
        """Create review mode user interface"""
        difficult_list = self.app.user_stats.get_difficult_words()
        due_list = self.app.user_stats.get_due_words()

        # Build lookup for full word objects from korean string
        all_words = self.app.vocabulary_data.get_all_words()
        word_lookup = {w["korean"]: w for w in all_words}

        # Build difficult words list (with error counts)
        self.review_words = []
        for korean_word, count in difficult_list:
            if korean_word in word_lookup:
                word_copy = word_lookup[korean_word].copy()
                word_copy["errors"] = count
                self.review_words.append(word_copy)

        # Build SRS due words list (words overdue for review)
        self.due_words = []
        for entry in due_list:
            korean = entry["korean"]
            if korean in word_lookup:
                word_copy = word_lookup[korean].copy()
                word_copy["days_overdue"] = entry["days_overdue"]
                self.due_words.append(word_copy)

        if not self.review_words and not self.due_words:
            messagebox.showinfo("Great Job!",
                "Nothing needs review right now.\n\nPlay Quiz mode to build your review queue.")
            self.app.show_main_menu()
            return

        # --- Top Bar ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Button(top_frame, text="← Back to Menu",
                  command=self.app.show_main_menu).pack(side=tk.LEFT)

        total = len(self.review_words) + len(self.due_words)
        tk.Label(top_frame, text=f"Needs Review ({total})",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20)

        tk.Button(top_frame, text="Start Practice Quiz ►",
                  bg="#e1f5fe", font=("Arial", 11, "bold"),
                  command=self.start_practice).pack(side=tk.RIGHT)

        # --- Scrollable List ---
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # --- SRS Due Words Section ---
        if self.due_words:
            tk.Label(scrollable_frame, text="Due for review today (SRS):",
                     font=("Arial", 10, "italic"), fg="#b36200").pack(pady=(10, 2), anchor="w")

            for word in self.due_words:
                row = tk.Frame(scrollable_frame, bg="#fff8e1", relief=tk.RIDGE, bd=1)
                row.pack(fill=tk.X, pady=3, padx=5, ipady=5)

                tk.Label(row, text=word["korean"], font=("Arial", 14, "bold"),
                         bg="#fff8e1", width=15, anchor="w").pack(side=tk.LEFT, padx=10)
                tk.Label(row, text=word["english"], font=("Arial", 12),
                         bg="#fff8e1").pack(side=tk.LEFT, padx=10)

                overdue = word["days_overdue"]
                label = "due today" if overdue == 0 else f"{overdue}d overdue"
                tk.Label(row, text=label, font=("Arial", 10),
                         fg="#b36200", bg="#fff8e1").pack(side=tk.RIGHT, padx=10)

        # --- Difficult Words Section ---
        if self.review_words:
            tk.Label(scrollable_frame, text="Words you've missed in quizzes:",
                     font=("Arial", 10, "italic"), fg="gray").pack(pady=(10, 2), anchor="w")

            for word in self.review_words:
                row = tk.Frame(scrollable_frame, bg="white", relief=tk.RIDGE, bd=1)
                row.pack(fill=tk.X, pady=3, padx=5, ipady=5)

                tk.Label(row, text=word["korean"], font=("Arial", 14, "bold"),
                         bg="white", width=15, anchor="w").pack(side=tk.LEFT, padx=10)
                tk.Label(row, text=word["english"], font=("Arial", 12),
                         bg="white").pack(side=tk.LEFT, padx=10)
                tk.Label(row, text=f"{word['errors']} mistakes", font=("Arial", 10),
                         fg="red", bg="white").pack(side=tk.RIGHT, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def start_practice(self):
        """Start a quiz using difficult words + SRS due words combined"""
        from gui.quiz import QuizMode

        # Merge difficult words and SRS due words, de-duplicating by korean key
        seen = set()
        combined = []
        for word in self.due_words + self.review_words:
            if word["korean"] not in seen:
                seen.add(word["korean"])
                combined.append(word)

        quiz = QuizMode(self.root, self.app, self.difficulty)
        quiz.quiz_words = combined
        random.shuffle(quiz.quiz_words)
        quiz.current_index = 0
        quiz.score = 0
        quiz.score_label.config(text=f"Score: 0/{len(quiz.quiz_words)}")
        quiz.show_question()