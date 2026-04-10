import os
from flask import Flask
from data.vocabulary import VocabularyData
from data.grammar import GrammarData
from models.user_stats import UserStats

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "korean-learning-dev-secret")

    app.vocab_data = VocabularyData()
    app.grammar_data = GrammarData()
    app.user_stats = UserStats()

    from routes.home import home_bp
    from routes.flashcards import flashcards_bp
    from routes.quiz import quiz_bp
    from routes.grammar import grammar_bp
    from routes.review import review_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(flashcards_bp, url_prefix="/flashcards")
    app.register_blueprint(quiz_bp, url_prefix="/quiz")
    app.register_blueprint(grammar_bp, url_prefix="/grammar")
    app.register_blueprint(review_bp, url_prefix="/review")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
