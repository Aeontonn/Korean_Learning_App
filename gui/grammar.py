# ============================================
# FILE: gui/grammar.py
# ============================================
import tkinter as tk
from tkinter import messagebox
import random

class GrammarMode:
    def __init__(self, root, app, difficulty):
        self.root = root
        self.app = app
        self.difficulty = difficulty
        
        patterns = self.app.grammar_data.get_patterns_by_difficulty(self.difficulty).copy()
        random.shuffle(patterns)
        
        self.patterns = patterns
        self.current_index = 0
        self.score = 0
        
        self.clear_window()
        self.create_ui()
        self.show_question()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_ui(self):
        # Top bar
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)
        
        back_btn = tk.Button(top_frame, text="← Back to Menu", 
                           command=self.app.show_main_menu)
        back_btn.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(top_frame, text=f"Score: 0/{len(self.patterns)}", 
                                  font=("Arial", 12))
        self.score_label.pack(side=tk.RIGHT)
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def show_question(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if self.current_index >= len(self.patterns):
            self.finish_grammar()
            return
            
        pattern = self.patterns[self.current_index]
        
        # UI Elements
        tk.Label(self.content_frame, text=f"Hint: {pattern['explanation']}",
               font=("Arial", 14), fg="blue").pack(pady=15)
        
        tk.Label(self.content_frame, text=f"Fill in the blank:\n\n{pattern['example']}",
               font=("Arial", 18)).pack(pady=15)
               
        tk.Label(self.content_frame, text=f"Translation: {pattern['translation']}",
               font=("Arial", 12), fg="gray").pack(pady=5)
        
        # Input Area
        entry_frame = tk.Frame(self.content_frame)
        entry_frame.pack(pady=15)
        
        tk.Label(entry_frame, text="Answer:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.answer_entry = tk.Entry(entry_frame, font=("Arial", 14), width=15)
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.focus()
        
        # Feedback Label (Empty at start)
        self.feedback_label = tk.Label(self.content_frame, text="", font=("Arial", 12, "bold"))
        self.feedback_label.pack(pady=10)
        
        # Submit Button
        self.action_btn = tk.Button(self.content_frame, text="Submit", font=("Arial", 14),
                                  command=lambda: self.check_answer(pattern))
        self.action_btn.pack(pady=10)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.action_btn.invoke())

    def check_answer(self, pattern):
        user_answer = self.answer_entry.get().strip()
        
        # If button is in "Next" mode, go to next question
        if self.action_btn['text'] == "Next Question →":
            self.root.unbind('<Return>') # Unbind enter key for a moment
            self.current_index += 1
            self.show_question()
            return

        # Check logic — normalize whitespace so minor spacing differences don't fail the user
        def normalize(s):
            return " ".join(s.split())

        if normalize(user_answer) == normalize(pattern["answer"]):
            self.score += 1
            self.app.user_stats.mark_correct()
            self.feedback_label.config(text="Correct! 🎉", fg="green")
            self.answer_entry.config(bg="#d0f0c0") # Light green background
        else:
            self.app.user_stats.mark_incorrect()
            self.feedback_label.config(text=f"Incorrect. The answer is '{pattern['answer']}'", fg="red")
            self.answer_entry.config(bg="#ffcccc") # Light red background
            
        self.score_label.config(text=f"Score: {self.score}/{len(self.patterns)}")
        
        # Change button to Next
        self.action_btn.config(text="Next Question →", bg="#e0e0e0")
        self.answer_entry.config(state="disabled") # Lock the input

    def finish_grammar(self):
        percentage = (self.score / len(self.patterns)) * 100
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.content_frame, text="Practice Complete!", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.content_frame, text=f"Final Score: {self.score}/{len(self.patterns)}", 
               font=("Arial", 18)).pack(pady=10)
        
        tk.Button(self.content_frame, text="Return to Menu", font=("Arial", 14),
                command=self.app.show_main_menu).pack(pady=30)