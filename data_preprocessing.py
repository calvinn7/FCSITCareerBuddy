import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


# Function to preprocess text data
def preprocess_text(text):


    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    # Join tokens back into text
    preprocessed_text = ' '.join(lemmatized_tokens)
    
    return preprocessed_text


def load_job_data(file_path):
    job_data = pd.read_csv(file_path)

    # Drop rows with NaN values in the 'summary' column
    job_data = job_data.dropna(subset=['summary'])

    # Data preprocessing
    job_data['summary'] = job_data['summary'].apply(preprocess_text)
    return job_data

def load_events(file_path):
    job_data = pd.read_csv(file_path)

    return job_data
