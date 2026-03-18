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
        # Check if there are difficult words
        difficult_list = self.app.user_stats.get_difficult_words()
        
        if not difficult_list:
            messagebox.showinfo("Great Job!", 
                              "You haven't marked any words as difficult yet.\n\nGo play the Quiz mode, and if you get any wrong, they will appear here!")
            self.app.show_main_menu()
            return
        
        # Match the difficult words (korean string) to full word objects
        self.review_words = []
        all_words = self.app.vocabulary_data.get_all_words()
        
        for korean_word, count in difficult_list:
            for w in all_words:
                if w["korean"] == korean_word:
                    # Create a copy so we don't modify original data
                    word_copy = w.copy()
                    word_copy['errors'] = count
                    self.review_words.append(word_copy)
                    break
        
        # --- Top Bar ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)
        
        back_btn = tk.Button(top_frame, text="← Back to Menu", 
                           command=self.app.show_main_menu)
        back_btn.pack(side=tk.LEFT)
        
        title = tk.Label(top_frame, text=f"Needs Review ({len(self.review_words)})", 
                        font=("Arial", 16, "bold"))
        title.pack(side=tk.LEFT, padx=20)

        # --- Practice Button ---
        practice_btn = tk.Button(top_frame, text="Start Practice Quiz ►", 
                               bg="#e1f5fe", font=("Arial", 11, "bold"),
                               command=self.start_practice)
        practice_btn.pack(side=tk.RIGHT)

        # --- List Area (Scrollable) ---
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

        # Draw the List
        tk.Label(scrollable_frame, text="Words you missed in Quizzes:", font=("Arial", 10, "italic"), fg="gray").pack(pady=5, anchor="w")

        for word in self.review_words:
            row = tk.Frame(scrollable_frame, bg="white", relief=tk.RIDGE, bd=1)
            row.pack(fill=tk.X, pady=5, padx=5, ipady=5)
            
            # Korean
            tk.Label(row, text=word['korean'], font=("Arial", 14, "bold"), bg="white", width=15, anchor="w").pack(side=tk.LEFT, padx=10)
            
            # English
            tk.Label(row, text=word['english'], font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=10)
            
            # Error Count
            tk.Label(row, text=f"{word['errors']} mistakes", font=("Arial", 10), fg="red", bg="white").pack(side=tk.RIGHT, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def start_practice(self):
        """Start a quiz using only the difficult words"""
        from gui.quiz import QuizMode
        
        # Override the quiz init logic slightly by passing custom words
        # Since QuizMode init usually loads from DB, we will instantiate it
        # then manually inject the difficult words.
        
        quiz = QuizMode(self.root, self.app, self.difficulty)
        quiz.quiz_words = self.review_words # Use our specific review list
        random.shuffle(quiz.quiz_words)
        quiz.current_index = 0
        quiz.score = 0
        quiz.score_label.config(text=f"Score: 0/{len(quiz.quiz_words)}")
        quiz.show_question()