class VocabularyData:
    def __init__(self):
        self.vocabulary = {
            "basic": [
                {"korean": "안녕하세요", "english": "hello", "category": "greetings"},
                {"korean": "감사합니다", "english": "thank you", "category": "greetings"},
                {"korean": "네", "english": "yes", "category": "basic"},
                {"korean": "아니요", "english": "no", "category": "basic"},
                {"korean": "죄송합니다", "english": "sorry", "category": "greetings"},
                {"korean": "안녕히 가세요", "english": "goodbye (to person leaving)", "category": "greetings"},
                {"korean": "안녕히 계세요", "english": "goodbye (to person staying)", "category": "greetings"},
                {"korean": "괜찮아요", "english": "it's okay", "category": "basic"},
                {"korean": "좋아요", "english": "good/like", "category": "basic"},
                {"korean": "싫어요", "english": "dislike", "category": "basic"},
                {"korean": "몰라요", "english": "I don't know", "category": "basic"},
                {"korean": "알아요", "english": "I know", "category": "basic"},
                {"korean": "도와주세요", "english": "please help me", "category": "basic"},
                {"korean": "축하합니다", "english": "congratulations", "category": "greetings"},
                {"korean": "생일 축하합니다", "english": "happy birthday", "category": "greetings"},
                {"korean": "먹다", "english": "to eat", "category": "verbs"},
                {"korean": "마시다", "english": "to drink", "category": "verbs"},
                {"korean": "가다", "english": "to go", "category": "verbs"},
                {"korean": "오다", "english": "to come", "category": "verbs"},
                {"korean": "보다", "english": "to see/watch", "category": "verbs"},
                {"korean": "듣다", "english": "to listen/hear", "category": "verbs"},
                {"korean": "읽다", "english": "to read", "category": "verbs"},
                {"korean": "쓰다", "english": "to write/use", "category": "verbs"},
                {"korean": "하다", "english": "to do", "category": "verbs"},
                {"korean": "말하다", "english": "to speak", "category": "verbs"},
                {"korean": "좋다", "english": "to be good", "category": "adjectives"},
                {"korean": "나쁘다", "english": "to be bad", "category": "adjectives"},
                {"korean": "크다", "english": "to be big", "category": "adjectives"},
                {"korean": "작다", "english": "to be small", "category": "adjectives"},
                {"korean": "아름답다", "english": "to be beautiful", "category": "adjectives"},
                {"korean": "예쁘다", "english": "to be pretty", "category": "adjectives"},
                {"korean": "맛있다", "english": "to be delicious", "category": "adjectives"},
                {"korean": "재미있다", "english": "to be fun/interesting", "category": "adjectives"},
                {"korean": "물", "english": "water", "category": "food"},
                {"korean": "밥", "english": "rice/meal", "category": "food"},
                {"korean": "김치", "english": "kimchi", "category": "food"},
                {"korean": "커피", "english": "coffee", "category": "food"},
                {"korean": "빵", "english": "bread", "category": "food"},
                {"korean": "우유", "english": "milk", "category": "food"},
                {"korean": "학교", "english": "school", "category": "places"},
                {"korean": "집", "english": "house/home", "category": "places"},
                {"korean": "회사", "english": "company/office", "category": "places"},
                {"korean": "병원", "english": "hospital", "category": "places"},
                {"korean": "친구", "english": "friend", "category": "people"},
                {"korean": "가족", "english": "family", "category": "people"},
                {"korean": "선생님", "english": "teacher", "category": "people"},
                {"korean": "학생", "english": "student", "category": "people"},
                {"korean": "오늘", "english": "today", "category": "time"},
                {"korean": "내일", "english": "tomorrow", "category": "time"},
                {"korean": "어제", "english": "yesterday", "category": "time"},
                {"korean": "지금", "english": "now", "category": "time"},
                {"korean": "언제", "english": "when", "category": "time"},
                {"korean": "어디", "english": "where", "category": "basic"},
                {"korean": "누구", "english": "who", "category": "basic"},
                {"korean": "무엇", "english": "what", "category": "basic"},
                {"korean": "왜", "english": "why", "category": "basic"},
                {"korean": "어떻게", "english": "how", "category": "basic"},
                
            ],
            "intermediate": [
                {"korean": "경험", "english": "experience", "category": "nouns"},
                {"korean": "노력하다", "english": "to make an effort / to try hard", "category": "verbs"},
                {"korean": "복잡하다", "english": "to be complicated / crowded", "category": "adjectives"},
                {"korean": "결정하다", "english": "to decide", "category": "verbs"},
                {"korean": "환경", "english": "environment", "category": "nouns"},
                {"korean": "익숙하다", "english": "to be familiar with / to be used to", "category": "adjectives"},
                {"korean": "설명하다", "english": "to explain", "category": "verbs"},
                {"korean": "당연하다", "english": "to be natural / reasonable / obvious", "category": "adjectives"},
                {"korean": "이해하다", "english": "to understand", "category": "verbs"},
                {"korean": "건강", "english": "health", "category": "nouns"} 
            ],
            "advanced": [
                {"korean": "현상", "english": "phenomenon", "category": "nouns"},
                {"korean": "평가하다", "english": "to evaluate / to assess", "category": "verbs"},
                {"korean": "해결하다", "english": "to resolve / to solve (a problem)", "category": "verbs"},
                {"korean": "불가피하다", "english": "to be inevitable / unavoidable", "category": "adjectives"},
                {"korean": "영향을 미치다", "english": "to influence / to have an effect on", "category": "phrases"},
                {"korean": "책임감", "english": "sense of responsibility", "category": "nouns"},
                {"korean": "모순", "english": "contradiction", "category": "nouns"},
                {"korean": "파악하다", "english": "to grasp / to figure out / to comprehend", "category": "verbs"},
                {"korean": "다양성", "english": "diversity", "category": "nouns"},
                {"korean": "활용하다", "english": "to utilize / to put to practical use", "category": "verbs"}
            ]
        }
    
    def get_words(self, difficulty):
        """Get words for a specific difficulty level only"""
        return self.vocabulary.get(difficulty, [])

    def get_words_cumulative(self, difficulty):
        """Get words for a difficulty level cumulatively.
        Intermediate includes basic. Advanced includes everything.
        This keeps flashcards and quiz consistent with each other."""
        if difficulty == "advanced":
            return self.get_all_words()
        elif difficulty == "intermediate":
            return self.get_words("basic") + self.get_words("intermediate")
        else:
            return self.get_words("basic")

    def get_all_words(self):
        """Get all words from all difficulty levels"""
        all_words = []
        for words in self.vocabulary.values():
            all_words.extend(words)
        return all_words
