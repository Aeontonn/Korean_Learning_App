# ============================================
# FILE: gui/quiz.py
# ============================================
import tkinter as tk
from tkinter import messagebox
import random

class QuizMode:
    def __init__(self, root, app, difficulty):
        self.root = root
        self.app = app
        self.difficulty = difficulty
        
        # 1. Determine the pool of words based on the selected difficulty
        if self.difficulty == "advanced":
            # Advanced gets the entire dictionary
            self.word_pool = self.app.vocabulary_data.get_all_words()
            
        elif self.difficulty == "intermediate":
            # Intermediate gets Basic + Intermediate words combined
            basic_words = self.app.vocabulary_data.get_words("basic")
            int_words = self.app.vocabulary_data.get_words("intermediate")
            
            # This is the list concatenation in action!
            self.word_pool = basic_words + int_words
            
        else:
            # If it's not advanced or intermediate, it must be basic
            self.word_pool = self.app.vocabulary_data.get_words("basic")
            
        # 2. Create a separate copy for the actual quiz questions so we can shuffle them
        words = self.word_pool.copy()
        
        # 3. Shuffle the final list of questions
        random.shuffle(words)
        
        self.quiz_words = words[:50]
        self.current_index = 0
        self.score = 0
        
        self.clear_window()
        self.create_ui()
        self.show_question()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_ui(self):
        # --- Top Bar ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)
        
        back_btn = tk.Button(top_frame, text="← Back to Menu", 
                           command=self.app.show_main_menu)
        back_btn.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(top_frame, text=f"Score: 0/{len(self.quiz_words)}", 
                                  font=("Arial", 12))
        self.score_label.pack(side=tk.RIGHT)
        
        # --- Content Area ---
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Question Label
        self.question_label = tk.Label(self.content_frame, text="", font=("Arial", 18))
        self.question_label.pack(pady=15)

        # Options Container
        self.options_frame = tk.Frame(self.content_frame)
        self.options_frame.pack(pady=5)
        
        # Feedback Label
        self.feedback_label = tk.Label(self.content_frame, text="", font=("Arial", 14, "bold"))
        self.feedback_label.pack(pady=10)

        # --- Next Button (Always Visible) ---
        self.next_btn = tk.Button(self.content_frame, text="Next Question →", 
                                font=("Arial", 12, "bold"), bg="#e0e0e0",
                                command=self.next_question, state="disabled") # Starts disabled
        self.next_btn.pack(pady=10, ipady=5, ipadx=10)

    def show_question(self):
        # Check if finished
        if self.current_index >= len(self.quiz_words):
            self.finish_quiz()
            return
        
        # Reset UI state
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.feedback_label.config(text="")
        self.next_btn.config(state="disabled", bg="#f0f0f0", text="Next Question →")
        
        current_word = self.quiz_words[self.current_index]
        
        # Update Question Text
        self.question_label.config(text=f"What is the English meaning of:\n\n{current_word['korean']}")
        
        # Generate Choices
        correct_answer = current_word["english"]
        
        # Use the pre-loaded pool of words instead of fetching them again
        all_words = self.word_pool
        
        # Filter out the correct answer from potential wrong answers
        wrong_answers = [w["english"] for w in all_words if w["english"] != correct_answer]
        
        # OPTIMIZATION: Pick exactly 3 wrong answers without shuffling the whole list
        selected_wrong_answers = random.sample(wrong_answers, 3)
        
        # Combine the correct answer with the 3 wrong answers
        choices = [correct_answer] + selected_wrong_answers
        
        # Shuffle the final 4 choices so the correct answer isn't always the first option
        random.shuffle(choices)
        
        # Create Choice Buttons
        self.option_buttons = []
        for choice in choices:
            btn = tk.Button(self.options_frame, text=choice, font=("Arial", 14),
                          width=30, height=2)
            # Bind the click
            btn.config(command=lambda c=choice, b=btn: self.check_answer(c, correct_answer, current_word, b))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

    def check_answer(self, selected, correct, word, clicked_btn):
        # 1. Lock all option buttons so you can't click again
        for btn in self.option_buttons:
            btn.config(state="disabled")
            # Highlight the correct answer in Green
            if btn['text'] == correct:
                btn.config(bg="#90EE90")  # Light Green

        # 2. Check Logic
        if selected == correct:
            self.score += 1
            self.app.user_stats.mark_correct(word['korean'])
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.app.user_stats.mark_incorrect(word['korean'])
            # Highlight the user's WRONG answer in Red
            clicked_btn.config(bg="#FFB6C1") # Light Red
            self.feedback_label.config(text=f"Incorrect. The answer was '{correct}'", fg="red")
        
        # 3. Update Score Display
        self.score_label.config(text=f"Score: {self.score}/{len(self.quiz_words)}")
        
        # 4. Enable the Next Button
        self.next_btn.config(state="normal", bg="#add8e6") # Blue-ish active color

    def next_question(self):
        self.current_index += 1
        self.show_question()

    def finish_quiz(self):
        # Clear content area
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        percentage = (self.score / len(self.quiz_words)) * 100 if len(self.quiz_words) > 0 else 0
        
        tk.Label(self.content_frame, text="Quiz Complete!", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.content_frame, text=f"Final Score: {self.score}/{len(self.quiz_words)}", 
               font=("Arial", 18)).pack(pady=10)
        tk.Label(self.content_frame, text=f"({percentage:.1f}%)", font=("Arial", 16), fg="gray").pack()
        
        tk.Button(self.content_frame, text="Return to Menu", font=("Arial", 14),
                command=self.app.show_main_menu).pack(pady=30)