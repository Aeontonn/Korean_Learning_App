# Korean Language Learning App 🇰🇷

A lightweight, interactive desktop application built with Python and Tkinter designed to help users study and master the Korean language. 

This project moves beyond simple flashcards by incorporating dynamic multiple-choice quizzes, targeted grammar practice, and an adaptive system that tracks and re-tests difficult vocabulary.

## 🚀 Features

* **Vocabulary Quizzes (Cumulative Difficulty):** Test your knowledge across Basic, Intermediate, and Advanced tiers. Higher difficulties automatically pool words from previous tiers to ensure foundational knowledge is retained. Multiple-choice options are dynamically generated to avoid repetition.
* **Grammar Practice Mode:** A fill-in-the-blank game focusing on sentence structure, particles (은/는, 이/가), and verb connectors. The UI cleanly separates hints from the core patterns to challenge active recall.
* **Interactive Flashcards:** A dedicated study mode for reviewing vocabulary before jumping into the testing phases.
* **Difficult Words Practice:** The application tracks user statistics (correct/incorrect answers) during quizzes. This specialized mode isolates the words you struggle with the most, allowing for highly targeted review sessions.

## 🛠️ Built With

* **Python 3.x:** Core application logic and data structures.
* **Tkinter:** Standard GUI library used for rendering the graphical interface, managing window states, and handling user inputs.

## 📦 Installation & Usage

Because this app relies entirely on Python's standard library, there are no external dependencies or packages to install!

1. Clone the repository:
    git clone https://github.com/YourUsername/korean-learning-app.git

2. Navigate to the project directory:
    cd korean-learning-app

3. Run the application:
    python main.py 

    *(Note: Depending on your system, you may need to use `python3 main.py`)*

## 📂 Project Structure

The codebase is organized with a strict separation of concerns, keeping the user interface logic separate from the data dictionaries.

* `main.py` - The entry point that initializes the app and root window.
* `gui/` - Contains the logic for the different screens (Menu, Quiz, Grammar, Flashcards).
* `data/` - (Future implementation) Dedicated files for storing vocabulary and grammar patterns, ensuring the UI code remains clean and scalable.

## 🌱 Future Improvements

* Migrate raw Python dictionaries into dedicated `.json` files for easier data management.
* Implement persistent local storage (saving user stats to a file) so "Difficult Words" are remembered between sessions.
* Add a timer mechanic to the Advanced vocabulary quizzes.

---
*Built as a personal project to combine software engineering practice with language learning.*
