import tkinter as tk
from tkinter import messagebox
import random

class FlashcardMode:
    def __init__(self, root, app, difficulty):
        self.root = root
        self.app = app
        self.difficulty = difficulty
        
        # Get and shuffle words — cumulative so intermediate includes basic, etc.
        words = self.app.vocabulary_data.get_words_cumulative(difficulty).copy()
        random.shuffle(words)
        
        self.flashcards = words
        self.current_index = 0
        self.show_korean = True
        
        self.clear_window()
        self.create_ui()
        self.display_current_card()
    
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
        
        self.progress_label = tk.Label(top_frame, text="", font=("Arial", 12))
        self.progress_label.pack(side=tk.RIGHT)
        
        # Flashcard Area
        card_container = tk.Frame(self.root)
        card_container.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        self.card_frame = tk.Frame(card_container, bg="white", relief=tk.RAISED, borderwidth=3)
        self.card_frame.pack(expand=True, fill=tk.BOTH)
        
        self.card_label = tk.Label(self.card_frame, text="", font=("Arial", 36, "bold"), 
                                   bg="white", wraplength=500)
        self.card_label.pack(expand=True)
        
        self.sub_label = tk.Label(self.card_frame, text="(Click to flip)", 
                                font=("Arial", 10), fg="gray", bg="white")
        self.sub_label.pack(pady=10)
        
        # Bind click events
        self.card_frame.bind("<Button-1>", lambda e: self.flip_card())
        self.card_label.bind("<Button-1>", lambda e: self.flip_card())
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=30)
        
        prev_btn = tk.Button(nav_frame, text="← Previous", font=("Arial", 12), width=12,
                           command=self.previous_card)
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        next_btn = tk.Button(nav_frame, text="Next →", font=("Arial", 12), width=12,
                           command=self.next_card)
        next_btn.pack(side=tk.LEFT, padx=10)

    def display_current_card(self):
        if self.current_index < len(self.flashcards):
            word = self.flashcards[self.current_index]
            text = word["korean"] if self.show_korean else word["english"]
            
            self.card_label.config(text=text, fg="black" if self.show_korean else "blue")
            self.progress_label.config(text=f"Card {self.current_index + 1}/{len(self.flashcards)}")
        else:
            messagebox.showinfo("Complete!", "You've finished the stack!")
            self.app.show_main_menu()
    
    def flip_card(self):
        self.show_korean = not self.show_korean
        self.display_current_card()
    
    def next_card(self):
        if self.current_index < len(self.flashcards) - 1:
            self.current_index += 1
            self.show_korean = True
            self.display_current_card()
    
    def previous_card(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_korean = True
            self.display_current_card()