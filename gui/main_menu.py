import tkinter as tk

class MainMenu:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.difficulty = tk.StringVar(value="intermediate")
        
        self.clear_window()
        self.create_ui()
    
    def clear_window(self):
        """Remove all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_ui(self):
        """Create main menu user interface"""
        # Title
        title = tk.Label(self.root, text="한국어 학습 앱", font=("Arial", 24, "bold"))
        title.pack(pady=30)
        
        subtitle = tk.Label(self.root, text="Korean Language Learning App", font=("Arial", 16))
        subtitle.pack(pady=10)
        
        # Stats display
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=20)
        
        correct_label = tk.Label(stats_frame, text=f"✓ Correct: {self.app.user_stats.correct}", 
                                font=("Arial", 12), fg="green")
        correct_label.grid(row=0, column=0, padx=20)
        
        incorrect_label = tk.Label(stats_frame, text=f"✗ Incorrect: {self.app.user_stats.incorrect}", 
                                  font=("Arial", 12), fg="red")
        incorrect_label.grid(row=0, column=1, padx=20)
        
        streak_label = tk.Label(stats_frame, text=f"🔥 Streak: {self.app.user_stats.streak}", 
                               font=("Arial", 12), fg="orange")
        streak_label.grid(row=0, column=2, padx=20)
        
        # Difficulty selection
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=20)
        
        tk.Label(difficulty_frame, text="Difficulty Level:", font=("Arial", 12)).pack()
        
        difficulties = ["basic", "intermediate", "advanced"]
        
        for diff in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=diff.capitalize(), 
                               variable=self.difficulty, value=diff,
                               font=("Arial", 11))
            rb.pack(side=tk.LEFT, padx=10)
        
        # Mode buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)
        
        flashcard_btn = tk.Button(button_frame, text="📚 Flashcards", 
                                  font=("Arial", 14), width=20, height=2,
                                  command=lambda: self.app.start_flashcard_mode(self.difficulty.get()))
        flashcard_btn.grid(row=0, column=0, padx=10, pady=10)
        
        quiz_btn = tk.Button(button_frame, text="❓ Multiple Choice Quiz", 
                            font=("Arial", 14), width=20, height=2,
                            command=lambda: self.app.start_quiz_mode(self.difficulty.get()))
        quiz_btn.grid(row=0, column=1, padx=10, pady=10)
        
        grammar_btn = tk.Button(button_frame, text="📝 Grammar Practice", 
                               font=("Arial", 14), width=20, height=2,
                               command=lambda: self.app.start_grammar_mode(self.difficulty.get()))
        grammar_btn.grid(row=1, column=0, padx=10, pady=10)
        
        review_btn = tk.Button(button_frame, text="🔄 Review Difficult Words", 
                              font=("Arial", 14), width=20, height=2,
                              command=lambda: self.app.start_review_mode(self.difficulty.get()))
        review_btn.grid(row=1, column=1, padx=10, pady=10)
