class GrammarData:
    def __init__(self):
        self.patterns = [
            # --- BASIC: Core particles and connectors ---
            {
                "pattern": "",
                "explanation": "Topic marker",
                "example": "저___ 학생입니다",
                "answer": "는",
                "translation": "I am a student",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "Subject marker",
                "example": "물___ 있어요",
                "answer": "이",
                "translation": "There is water",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "Object marker",
                "example": "밥___ 먹어요",
                "answer": "을",
                "translation": "I eat rice",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "Location/time marker",
                "example": "학교___ 가요",
                "answer": "에",
                "translation": "I go to school",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "And (connects verbs)",
                "example": "밥을 먹___ 물을 마셔요",
                "answer": "고",
                "translation": "I eat rice and drink water",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "Location of action",
                "example": "도서관___ 공부해요",
                "answer": "에서",
                "translation": "I study at the library",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "And (connects nouns)",
                "example": "친구___ 같이 가요",
                "answer": "하고",
                "translation": "I go together with a friend",
                "difficulty": "basic"
            },
            {
                "pattern": "",
                "explanation": "Sometimes / Occasionally",
                "example": "저는 ___ 도서관에 가요",
                "answer": "가끔",
                "translation": "I sometimes go to the library",
                "difficulty": "basic"
            },

            # --- INTERMEDIATE: Comparisons, continuous, suggestions, permission ---
            {
                "pattern": "",
                "explanation": "More than (Comparison)",
                "example": "수박이 사과___ 큽니다",
                "answer": "보다",
                "translation": "A watermelon is bigger than an apple",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "The most (Superlative)",
                "example": "이 영화가 ___ 재미있어요",
                "answer": "제일",
                "translation": "This movie is the most interesting",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "Am/Are/Is doing (Present continuous)",
                "example": "지금 책을 읽___",
                "answer": "고 있어요",
                "translation": "I am reading a book now",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "To become (Change of state with adjectives)",
                "example": "날씨가 추워___",
                "answer": "졌어요",
                "translation": "The weather became cold",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "Shall we...? / Do you think...?",
                "example": "우리 같이 영화를 볼___?",
                "answer": "까요",
                "translation": "Shall we watch a movie together?",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "Let's (Formal suggestion)",
                "example": "내일 만납___",
                "answer": "시다",
                "translation": "Let's meet tomorrow",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "Have to / Must",
                "example": "내일 일찍 일어나___",
                "answer": "야 해요",
                "translation": "I have to wake up early tomorrow",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "May I...? / Is it okay if...?",
                "example": "여기에 앉아___?",
                "answer": "도 돼요",
                "translation": "Is it okay if I sit here?",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "Because (Noun + because of)",
                "example": "비 ___ 못 갔어요",
                "answer": "때문에",
                "translation": "I couldn't go because of the rain",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "Before doing something",
                "example": "밥을 먹기 ___ 손을 씻어요",
                "answer": "전에",
                "translation": "I wash my hands before eating",
                "difficulty": "intermediate"
            },
            {
                "pattern": "",
                "explanation": "After doing something",
                "example": "수업이 끝난 ___ 만나요",
                "answer": "후에",
                "translation": "Let's meet after class ends",
                "difficulty": "intermediate"
            },

            # --- ADVANCED: Complex structures, experience, nuanced grammar ---
            {
                "pattern": "",
                "explanation": "Ended up doing (Change of state with verbs)",
                "example": "한국 음식을 잘 먹___",
                "answer": "게 되었어요",
                "translation": "I ended up being able to eat Korean food well",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "I think that... (Present tense verbs)",
                "example": "비가 오___",
                "answer": "는 것 같아요",
                "translation": "I think it is raining",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "You should not / You must not",
                "example": "여기서 사진을 찍으___",
                "answer": "면 안 돼요",
                "translation": "You must not take pictures here",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "Have done (Past experience)",
                "example": "한국에 가 ___",
                "answer": "본 적이 있어요",
                "translation": "I have been to Korea",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "Background info / 'But' (Verbs)",
                "example": "밥을 먹___, 맛이 없었어요",
                "answer": "는데",
                "translation": "I ate the food, but it wasn't good",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "To plan to do something",
                "example": "내일 친구를 만날 ___",
                "answer": "예정이에요",
                "translation": "I plan to meet a friend tomorrow",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "While doing something",
                "example": "음악을 들으___ 공부해요",
                "answer": "면서",
                "translation": "I study while listening to music",
                "difficulty": "advanced"
            },
            {
                "pattern": "",
                "explanation": "To know how to do something",
                "example": "한국어를 할 ___",
                "answer": "줄 알아요",
                "translation": "I know how to speak Korean",
                "difficulty": "advanced"
            },
        ]

    def get_all_patterns(self):
        """Get all grammar patterns"""
        return self.patterns

    def get_patterns_by_difficulty(self, difficulty):
        """Get patterns filtered by difficulty level (cumulative, like quiz mode)"""
        if difficulty == "advanced":
            return self.patterns
        elif difficulty == "intermediate":
            return [p for p in self.patterns if p["difficulty"] in ("basic", "intermediate")]
        else:
            return [p for p in self.patterns if p["difficulty"] == "basic"]
