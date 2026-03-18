import tkinter as tk
from models.user_stats import UserStats
from data.vocabulary import VocabularyData
from data.grammar import GrammarData
from gui.main_menu import MainMenu
from gui.flashcards import FlashcardMode
from gui.quiz import QuizMode
from gui.grammar import GrammarMode
from gui.review import ReviewMode

class KoreanLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Language Learning App")
        self.root.geometry("800x600")
        
        # Initialize data sources
        self.vocabulary_data = VocabularyData()
        self.grammar_data = GrammarData()
        self.user_stats = UserStats()
        
        # Start with main menu
        self.show_main_menu()
    
    def show_main_menu(self):
        """Display the main menu"""
        MainMenu(self.root, self)
    
    def start_flashcard_mode(self, difficulty):
        """Start flashcard practice mode"""
        FlashcardMode(self.root, self, difficulty)
    
    def start_quiz_mode(self, difficulty):
        """Start multiple choice quiz mode"""
        QuizMode(self.root, self, difficulty)
    
    def start_grammar_mode(self, difficulty):
        """Start grammar practice mode"""
        GrammarMode(self.root, self, difficulty)
    
    def start_review_mode(self, difficulty):
        """Start review of difficult words"""
        ReviewMode(self.root, self, difficulty)

