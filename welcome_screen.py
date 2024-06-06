from datetime import datetime
import streamlit as st

#define greeting based on time
def get_dynamic_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "🌞 Good Morning"
    elif 12 <= current_hour < 17:
        return "🌤 Good Afternoon"
    elif 17 <= current_hour < 21:
        return "🌙 Good Evening"
    else:
        return "👋🏻 Hello"

# List of motivational quotes or fun facts
motivational_quotes = [
    "🚀 'Your career is your business. It’s time for you to manage it as a CEO.' - Dorit Sher",
    "🌟 'The only way to do great work is to love what you do.' - Steve Jobs",    
    "💼 'Choose a job you love, and you will never have to work a day in your life.' - Confucius",
    "📈 'Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.' - Albert Schweitzer",
    "🌐 'Networking is not about just connecting people. It’s about connecting people with people, people with ideas, and people with opportunities.' - Michele Jennae",
    "🎯 'The future depends on what you do today.' - Mahatma Gandhi",
    "🌱 'The best way to predict the future is to create it.' - Peter Drucker",
    "🚴 'It does not matter how slowly you go as long as you do not stop.' - Confucius",
    "💡 'Innovation distinguishes between a leader and a follower.' - Steve Jobs",
    "🌍 'Your network is your net worth.' - Porter Gale",
    "🚀 'The only limit to our realization of tomorrow is our doubts of today.' - Franklin D. Roosevelt",
    "💪 'Believe you can and you're halfway there.' - Theodore Roosevelt",
    "🔗 'Opportunities don't happen. You create them.' - Chris Grosser",
    "🌠 'Dream big and dare to fail.' - Norman Vaughan",
    "🌱 'The journey of a thousand miles begins with one step.' - Lao Tzu",
    "🎓 'The beautiful thing about learning is that no one can take it away from you.' - B.B. King",
    "💬 'The way to get started is to quit talking and begin doing.' - Walt Disney",
    "🏆 'Don’t watch the clock; do what it does. Keep going.' - Sam Levenson",
    "🌟 'Success usually comes to those who are too busy to be looking for it.' - Henry David Thoreau",
    "🚀 'Act as if what you do makes a difference. It does.' - William James",
    "🌍 'The expert in anything was once a beginner.' - Helen Hayes",
    "🔗 'Success is walking from failure to failure with no loss of enthusiasm.' - Winston Churchill",
    "📈 'Do not be embarrassed by your failures, learn from them and start again.' - Richard Branson",
    "💼 'Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.' - Steve Jobs",
    "🌱 'Every job is a self-portrait of the person who did it. Autograph your work with excellence.' - Jessica Guidobono",
    "🎯 'Hard work beats talent when talent doesn’t work hard.' - Tim Notke",
    "💡 'The harder you work for something, the greater you’ll feel when you achieve it.' - Anonymous",
    "🚴 'Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.' - Christian D. Larson"
]

 # Select a random quote
import random

# Define welcome screen
def render_welcome_screen():
    dynamic_greeting = get_dynamic_greeting()
    selected_quote = random.choice(motivational_quotes)  

    gradient_text_html = f"""
    <style>
    .gradient-text {{
        font-weight: bold;
        background: -webkit-linear-gradient(left, rgb(51, 78, 255), rgb(197, 153, 233));
        background: linear-gradient(to right, rgb(51, 78, 255), rgb(197, 153, 233));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
    }}
    
    .quote {{
        font-style: italic;
        color: gray;
        margin-top: 10px;
    }}
    
    .footer {{
        margin-top: 20px;
        font-size: 0.9em;
        color: gray;
    }}

    .credits {{
        margin-top: 250px;
        font-size: 0.9em;
        color: gray;
        text-align: center;
    }}

    </style>
    <div class="gradient-text">{dynamic_greeting}, Welcome to the FCSIT Career Buddy</div>
    <div class="quote">{selected_quote}</div>
    """
    st.markdown(gradient_text_html, unsafe_allow_html=True)
    st.subheader("Your personal AI-powered career companion")

    st.markdown("""
    **FCSIT Career Buddy** is designed to help you with job recommendations, networking events, and application guidance.
    
    **How to Use:**
    - Ask any questions about job recommendations, networking events or internship application.
    - Use the chat interface to chat with your Career Buddy.
    - Click the button below to get started!
    """)

    if st.button("Start Chat"):
        st.session_state.show_welcome = False
        st.rerun()


    # Footer section
    st.markdown("""
    <div class="footer">
        <p>For more information, visit our <a href="https://careerportal.fsktm.um.edu.my" target="_blank">website</a>.</p>
    </div>
    """, unsafe_allow_html=True)

    # Credits section
    st.markdown("""
    <div class="credits">
        Developed by Calvin, Alyssa, Serene, Trishan, Jia Sheng, and Hua Qi
            \nNLP Assignment 2023/2024 Semester 2 @UM
    </div>
    """, unsafe_allow_html=True)
