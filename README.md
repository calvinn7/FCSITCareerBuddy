# 🌟 FCSIT CareerBuddy Chatbot
### WID3002 Natural Language Processing Assignment

Welcome to the FCSIT CareerBuddy Chatbot repository! This chatbot is an AI-powered career companion designed to assist students in navigating their career development journey within the Faculty of Computer Science and Information Technology (FSKTM) at University Malaya.


## 📚 Overview

The FCSIT CareerBuddy Chatbot provides students with personalized recommendations, comprehensive job information, and application guidance to streamline the internship and job search process. Leveraging natural language processing (NLP) techniques, the chatbot offers tailored support based on individual skills, interests, and career aspirations.

## ✨ Features

- **🎯 Personalized Recommendations**: Receive job recommendations based on your preferences.
- **📋 Comprehensive Information**: Access detailed job listings, company insights, and upcoming networking events.
- **📝 Application Guidance**: Get assistance with your application for internships.

## 💻 Tech Stack

- **Programming Languages**: Python
- **Libraries**: NLTK, pandas, scikit-learn, Streamlit, transformers, BERT
- **NLP Techniques**: Tokenization, Lemmatization, Spell Checking, Stopword Removal
- **Web Design**: HTML,CSS
- **Web Scrapping**: Selenium, BeautifulSoup

## 🚀 Installation and Setup
### Steps to Run the Chatbot Locally

1. **Clone the Repository**

    ```sh
    git clone https://github.com/calvinn7/FCSITCareerBuddy.git
    cd FCSITCareerBuddy
    ```
    
2. **Install the Required Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

3. **Download NLTK Resources**

    Run the following Python script to download the necessary NLTK resources:

    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    ```
    
4. **Training the Intent Classification Model**

    Before using the chatbot, you would need to train the intent classification model, it will take a few minutes:

    ```sh
    python train_intent_model.py
    ```

### Running the Chatbot

1. **Start the Streamlit Application**

    ```sh
    streamlit run app.py
    ```

2. **Open Your Browser**

    Go to `http://localhost:8501` to interact with the chatbot.

## 👥 Meet the Team

Meet the team behind the FCSIT CareerBuddy Chatbot:

- **Calvin** - Project Lead/Frontend/Backend
- **Alyssa** - Frontend
- **Trishan** - Backend
- **Serene** - Backend
- **Jia Sheng** - Backend
- **Hua Qi** - Backend

