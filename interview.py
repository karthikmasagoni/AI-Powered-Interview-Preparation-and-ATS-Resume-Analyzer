
def get_questions(role):

    questions = {

        "Python Developer": [

            "What is OOP in Python?",

            "Difference between List and Tuple?",

            "What are decorators?",

            "Explain Exception Handling.",

            "What is a Generator?"
        ],

        "AI/ML Engineer": [

            "What is Machine Learning?",

            "Difference between Supervised and Unsupervised Learning?",

            "What is Overfitting?",

            "Explain Random Forest.",

            "What is Gradient Descent?"
        ],

        "Data Analyst": [

            "What is Pandas?",

            "What is Data Cleaning?",

            "Explain GroupBy in Pandas.",

            "Difference between INNER JOIN and LEFT JOIN.",

            "What is Data Visualization?"
        ],

        "HR": [

            "Tell me about yourself.",

            "Why should we hire you?",

            "What are your strengths?",

            "What are your weaknesses?",

            "Where do you see yourself in 5 years?"
        ]
    }

    return questions.get(role, [])