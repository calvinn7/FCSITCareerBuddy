import random

#define the list of response for greeting
greet_responses = [
    "Hi there, I am your career buddy! How can I help you today?",
    "Hello! How can I assist you today?",
    "Hi! What can I do for you today?",
    "Greetings! How can I be of service today?",
    "Hello there! Ready to explore some career opportunities?",
    "Hey! Need help with your career journey?",
    "Hi! Looking for job recommendations or networking events?",
    "Good day! How can I support your career aspirations today?",
    "Hi! What brings you to career buddy today?",
    "Welcome! How can I make your job search easier?"
]

#define the list of responses for bye
bye_responses = [
    "Thank you for using career buddy! See you soon.",
    "Goodbye! Have a great day!",
    "See you later! Take care.",
    "Farewell! Hope to assist you again soon.",
    "Bye! Wishing you success in your career!",
    "Goodbye! Don't hesitate to come back for more career advice.",
    "Take care! Feel free to reach out anytime.",
    "Bye! Best of luck with your job search.",
    "Goodbye! Remember, I'm here whenever you need career assistance.",
    "See you! Keep striving for your career goals."
]

def get_greet_response():
    return random.choice(greet_responses)

def get_bye_response():
    return random.choice(bye_responses)